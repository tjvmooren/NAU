from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

LIKELY_USEFUL_FIELDS = [
    "EventID",
    "Provider",
    "Channel",
    "TimeCreated",
    "Computer",
    "Image",
    "CommandLine",
    "ParentImage",
    "User",
    "TargetObject",
    "DestinationIp",
    "DestinationHostname",
    "QueryName",
    "ScriptBlockText",
]

JSONPath = Sequence[str | int]


def read_text(path: str | Path) -> str:
    """Read text while handling UTF-8 BOM and odd characters gracefully."""
    return Path(path).read_text(encoding="utf-8-sig", errors="replace")


def load_json_array(path: str | Path) -> list[Any]:
    """Load a JSON file whose top-level payload is an array."""
    payload = json.loads(read_text(path))
    if not isinstance(payload, list):
        raise ValueError(f"{path} does not contain a top-level JSON array.")
    return payload


def load_ndjson(path: str | Path) -> list[Any]:
    """Load newline-delimited JSON, skipping blank lines."""
    events: list[Any] = []
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                message = (
                    f"Invalid JSON on line {line_number} of {file_path}: {exc.msg}"
                )
                raise ValueError(message) from exc

    return events


def detect_json_format(path: str | Path) -> str:
    """
    Detect whether a JSON file is a JSON array, NDJSON, a single JSON object,
    or effectively empty.
    """
    text = read_text(path).strip()
    if not text:
        return "empty"

    if text.startswith("["):
        payload = json.loads(text)
        if isinstance(payload, list):
            return "json_array"
        return "unknown"

    if not text.startswith("{"):
        return "unknown"

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        load_ndjson(path)
        return "ndjson"

    if isinstance(payload, dict):
        return "single_json_object"
    if isinstance(payload, list):
        return "json_array"

    return "unknown"


def load_json_events(path: str | Path, fmt: str | None = None) -> list[Any]:
    """Load events using the detected JSON layout."""
    format_name = fmt or detect_json_format(path)

    if format_name == "json_array":
        return load_json_array(path)
    if format_name == "ndjson":
        return load_ndjson(path)
    if format_name == "single_json_object":
        return [json.loads(read_text(path))]
    if format_name == "empty":
        return []

    raise ValueError(f"Unsupported JSON format for {path}: {format_name}")


def get_nested(
    data: Any,
    path: str | JSONPath,
    default: Any = None,
) -> Any:
    """Safely walk a nested dict/list structure."""
    if isinstance(path, str):
        parts: list[str | int] = [part for part in path.split(".") if part]
    else:
        parts = list(path)

    current = data
    for part in parts:
        if isinstance(current, Mapping):
            if part not in current:
                return default
            current = current[part]
            continue

        if isinstance(current, list) and isinstance(part, int):
            if part < 0 or part >= len(current):
                return default
            current = current[part]
            continue

        return default

    return current


def is_blank(value: Any) -> bool:
    """Treat None, empty strings, placeholder dashes, and empty containers as blank."""
    if value is None:
        return True
    if isinstance(value, str):
        normalized = value.strip()
        return normalized in {"", "-", "null", "None", "(null)"}
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def scalarize(value: Any) -> Any:
    """Unwrap common XML-to-JSON patterns such as {'#text': ...}."""
    if isinstance(value, Mapping):
        for key in ("#text", "@Name", "Value", "value"):
            if key in value:
                return scalarize(value[key])
        return value

    if isinstance(value, list):
        items = [scalarize(item) for item in value]
        items = [item for item in items if not is_blank(item)]
        if len(items) == 1:
            return items[0]
        return items

    if isinstance(value, str):
        text = html.unescape(value).strip()
        return text or None

    return value


def coalesce(*values: Any) -> Any:
    """Return the first non-blank value after normalizing simple wrappers."""
    for value in values:
        normalized = scalarize(value)
        if not is_blank(normalized):
            return normalized
    return None


def parse_embedded_json(value: Any) -> Any | None:
    """Parse JSON that is stored inside a string field like Payload."""
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text or text[0] not in "{[":
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def parse_key_value_text(text: str) -> dict[str, Any]:
    """
    Parse Windows event text blocks such as PowerShell EventData strings that
    store one key/value pair per line.
    """
    parsed: dict[str, Any] = {}
    unescaped = html.unescape(text)

    for raw_line in unescaped.splitlines():
        line = raw_line.strip().rstrip(",")
        if not line:
            continue

        if "=" in line:
            key, value = line.split("=", 1)
        elif ": " in line:
            key, value = line.split(": ", 1)
        else:
            continue

        key = key.strip()
        value = value.strip()
        if key and value:
            parsed[key] = value

    return parsed


def _extract_named_data_items(items: list[Any]) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    collected_text: list[str] = []

    for item in items:
        if not isinstance(item, Mapping):
            continue

        name = coalesce(item.get("@Name"), item.get("Name"), item.get("name"))
        value = coalesce(item.get("#text"), item.get("Value"), item.get("value"))

        if name is not None and value is not None:
            extracted[str(name)] = value
            continue

        if "#text" in item:
            text_value = scalarize(item.get("#text"))
            if not is_blank(text_value):
                collected_text.append(str(text_value))

    if collected_text:
        combined_text = "\n".join(collected_text)
        extracted["DataText"] = combined_text
        extracted.update(parse_key_value_text(combined_text))

    return extracted


def _extract_event_data_fields(event_data: Any) -> dict[str, Any]:
    if not isinstance(event_data, Mapping):
        return {}

    extracted: dict[str, Any] = {}
    data_value = event_data.get("Data")

    if isinstance(data_value, list):
        extracted.update(_extract_named_data_items(data_value))
    elif isinstance(data_value, str):
        extracted["DataText"] = html.unescape(data_value).strip()
        extracted.update(parse_key_value_text(data_value))
    elif isinstance(data_value, Mapping):
        for key, value in data_value.items():
            normalized = scalarize(value)
            if not is_blank(normalized):
                extracted[str(key)] = normalized

    for key, value in event_data.items():
        if key == "Data":
            continue
        normalized = scalarize(value)
        if not is_blank(normalized):
            extracted[str(key)] = normalized

    return extracted


def extract_event_data_fields(raw_event: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize common EventData shapes into a flat dictionary."""
    fields: dict[str, Any] = {}

    for key, value in raw_event.items():
        if key.startswith("PayloadData") and isinstance(value, str):
            fields.update(parse_key_value_text(value))

    payload = parse_embedded_json(raw_event.get("Payload"))
    if isinstance(payload, Mapping):
        fields.update(_extract_event_data_fields(payload.get("EventData", payload)))

    native_event_data = get_nested(raw_event, ["Event", "EventData"])
    fields.update(_extract_event_data_fields(native_event_data))

    direct_event_data = raw_event.get("EventData")
    fields.update(_extract_event_data_fields(direct_event_data))

    return fields


def flatten_windows_event(raw_event: Mapping[str, Any]) -> dict[str, Any]:
    """
    Flatten the most useful Windows event log fields into one dictionary for
    inspection and later feature engineering.
    """
    system = get_nested(raw_event, ["Event", "System"], default={})
    event_data_fields = extract_event_data_fields(raw_event)

    flattened = {
        "EventID": coalesce(
            raw_event.get("EventID"),
            raw_event.get("EventId"),
            get_nested(system, ["EventID", "#text"]),
            get_nested(system, ["EventID"]),
            event_data_fields.get("EventID"),
        ),
        "Provider": coalesce(
            raw_event.get("Provider"),
            get_nested(system, ["Provider", "@Name"]),
        ),
        "Channel": coalesce(
            raw_event.get("Channel"),
            get_nested(system, ["Channel"]),
        ),
        "TimeCreated": coalesce(
            raw_event.get("TimeCreated"),
            get_nested(system, ["TimeCreated", "@SystemTime"]),
            event_data_fields.get("UtcTime"),
        ),
        "Computer": coalesce(
            raw_event.get("Computer"),
            get_nested(system, ["Computer"]),
        ),
        "Image": coalesce(
            raw_event.get("Image"),
            event_data_fields.get("Image"),
            event_data_fields.get("ProcessName"),
        ),
        "CommandLine": coalesce(
            raw_event.get("CommandLine"),
            event_data_fields.get("CommandLine"),
            event_data_fields.get("HostApplication"),
            raw_event.get("ExecutableInfo"),
        ),
        "ParentImage": coalesce(
            raw_event.get("ParentImage"),
            event_data_fields.get("ParentImage"),
        ),
        "User": coalesce(
            raw_event.get("User"),
            event_data_fields.get("User"),
            raw_event.get("UserName"),
            event_data_fields.get("UserName"),
            event_data_fields.get("TargetUserName"),
            event_data_fields.get("SubjectUserName"),
        ),
        "TargetObject": coalesce(
            raw_event.get("TargetObject"),
            event_data_fields.get("TargetObject"),
        ),
        "DestinationIp": coalesce(
            raw_event.get("DestinationIp"),
            event_data_fields.get("DestinationIp"),
        ),
        "DestinationHostname": coalesce(
            raw_event.get("DestinationHostname"),
            event_data_fields.get("DestinationHostname"),
            event_data_fields.get("DestinationHostName"),
        ),
        "QueryName": coalesce(
            raw_event.get("QueryName"),
            event_data_fields.get("QueryName"),
        ),
        "ScriptBlockText": coalesce(
            raw_event.get("ScriptBlockText"),
            event_data_fields.get("ScriptBlockText"),
        ),
        "EventRecordID": coalesce(
            raw_event.get("EventRecordId"),
            raw_event.get("EventRecordID"),
            get_nested(system, ["EventRecordID"]),
        ),
        "SourceFile": coalesce(raw_event.get("SourceFile")),
        "MapDescription": coalesce(raw_event.get("MapDescription")),
        "EventDataFields": event_data_fields,
    }

    return {
        key: value
        for key, value in flattened.items()
        if key == "EventDataFields" or not is_blank(value)
    }
