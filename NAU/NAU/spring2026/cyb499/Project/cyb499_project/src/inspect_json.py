from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from utils import (
        LIKELY_USEFUL_FIELDS,
        detect_json_format,
        flatten_windows_event,
        is_blank,
        load_json_events,
    )
except ImportError:
    from src.utils import (
        LIKELY_USEFUL_FIELDS,
        detect_json_format,
        flatten_windows_event,
        is_blank,
        load_json_events,
    )

PROJECT_ROOT = Path(__file__).resolve().parents[1]
JSON_SUFFIXES = {".json", ".jsonl", ".ndjson"}
FORMAT_LABELS = {
    "ndjson": "newline-delimited JSON",
    "json_array": "JSON array",
    "single_json_object": "single JSON object",
    "empty": "empty or whitespace-only",
    "invalid": "invalid or unreadable",
    "unknown": "unknown",
}


@dataclass
class FieldSummary:
    present_count: int
    sample_values: list[str]


@dataclass
class FileInventory:
    bucket: str
    path: Path
    format_name: str
    event_count: int
    top_level_keys: list[tuple[str, int]] = field(default_factory=list)
    useful_fields: dict[str, FieldSummary] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect raw Windows Event Log JSON files without building a dataset.",
    )
    parser.add_argument(
        "--benign-dir",
        type=Path,
        default=Path("data/raw/benign"),
        help="Directory containing benign source JSON files.",
    )
    parser.add_argument(
        "--malicious-dir",
        type=Path,
        default=Path("data/raw/malicious"),
        help="Directory containing malicious-scenario source JSON files.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path("report_notes/json_inventory.md"),
        help="Where to save the Markdown summary report.",
    )
    parser.add_argument(
        "--top-key-limit",
        type=int,
        default=12,
        help="Maximum number of common top-level keys to show per file.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=3,
        help="Maximum number of sample values to show per useful field.",
    )
    return parser.parse_args()


def find_json_files(root: Path) -> list[Path]:
    if not root.exists():
        return []

    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in JSON_SUFFIXES
    ]
    return sorted(files)


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_project_path(path: Path) -> Path:
    """Resolve relative paths from the repository root instead of the launch cwd."""
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def stringify_sample(value: Any, limit: int = 120) -> str:
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(value)

    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def summarize_top_level_keys(
    events: list[Any],
    limit: int,
) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for event in events:
        if isinstance(event, dict):
            counter.update(event.keys())
        else:
            counter["<non-dict-event>"] += 1

    return counter.most_common(limit)


def summarize_useful_fields(
    flattened_events: list[dict[str, Any]],
    event_count: int,
    sample_limit: int,
) -> dict[str, FieldSummary]:
    summaries: dict[str, FieldSummary] = {}

    for field_name in LIKELY_USEFUL_FIELDS:
        present_count = 0
        samples: list[str] = []
        seen: set[str] = set()

        for event in flattened_events:
            value = event.get(field_name)
            if is_blank(value):
                continue

            present_count += 1
            sample = stringify_sample(value)
            if sample not in seen and len(samples) < sample_limit:
                seen.add(sample)
                samples.append(sample)

        if present_count > 0:
            summaries[field_name] = FieldSummary(
                present_count=present_count,
                sample_values=samples,
            )

    return summaries


def inspect_file(
    path: Path,
    bucket: str,
    top_key_limit: int,
    sample_limit: int,
) -> FileInventory:
    notes: list[str] = []

    try:
        format_name = detect_json_format(path)
    except (ValueError, json.JSONDecodeError) as exc:
        return FileInventory(
            bucket=bucket,
            path=path,
            format_name="invalid",
            event_count=0,
            notes=[f"Could not detect JSON format: {exc}"],
        )

    if format_name == "empty":
        return FileInventory(
            bucket=bucket,
            path=path,
            format_name=format_name,
            event_count=0,
            notes=["File is empty or contains only whitespace/BOM content."],
        )

    try:
        events = load_json_events(path, format_name)
    except (ValueError, json.JSONDecodeError) as exc:
        return FileInventory(
            bucket=bucket,
            path=path,
            format_name="invalid",
            event_count=0,
            notes=[f"Could not load JSON events: {exc}"],
        )

    if format_name == "single_json_object":
        notes.append(
            "Loaded as a single JSON object. This file is not NDJSON or a JSON array."
        )

    top_level_keys = summarize_top_level_keys(events, top_key_limit)

    flattened_events = [
        flatten_windows_event(event)
        for event in events
        if isinstance(event, dict)
    ]
    useful_fields = summarize_useful_fields(
        flattened_events=flattened_events,
        event_count=len(events),
        sample_limit=sample_limit,
    )

    non_dict_count = len(events) - len(flattened_events)
    if non_dict_count:
        notes.append(f"{non_dict_count} event(s) were not JSON objects.")

    return FileInventory(
        bucket=bucket,
        path=path,
        format_name=format_name,
        event_count=len(events),
        top_level_keys=top_level_keys,
        useful_fields=useful_fields,
        notes=notes,
    )


def build_markdown_report(inventories: list[FileInventory]) -> str:
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    format_counts = Counter(item.format_name for item in inventories)
    bucket_counts = Counter(item.bucket for item in inventories)

    lines = [
        "# JSON Inventory",
        "",
        f"Generated: `{generated_at}`",
        "",
        "This report is for dataset inspection only. It does not create labels or build the final dataset.",
        "",
        "Important note: files stored under `data/raw/malicious` are attack-scenario source files. Individual events should not be assumed malicious solely because of the folder they came from.",
        "",
        "## Summary",
        "",
        f"- JSON files inspected: {len(inventories)}",
        f"- Files under `benign`: {bucket_counts.get('benign', 0)}",
        f"- Files under `malicious`: {bucket_counts.get('malicious', 0)}",
    ]

    for format_name in sorted(format_counts):
        lines.append(
            f"- Format `{FORMAT_LABELS.get(format_name, format_name)}`: {format_counts[format_name]}"
        )

    for bucket in ("benign", "malicious"):
        bucket_items = [item for item in inventories if item.bucket == bucket]
        lines.extend(
            [
                "",
                f"## {bucket.capitalize()} Files",
                "",
            ]
        )

        if not bucket_items:
            lines.append("_No JSON files found._")
            continue

        for inventory in bucket_items:
            lines.extend(render_inventory_section(inventory))

    return "\n".join(lines) + "\n"


def render_inventory_section(inventory: FileInventory) -> list[str]:
    lines = [
        f"### `{repo_relative(inventory.path)}`",
        "",
        f"- Format: {FORMAT_LABELS.get(inventory.format_name, inventory.format_name)}",
        f"- Event count: {inventory.event_count}",
    ]

    if inventory.top_level_keys:
        common_keys = ", ".join(
            f"`{key}` ({count})" for key, count in inventory.top_level_keys
        )
        lines.append(f"- Common top-level keys: {common_keys}")
    else:
        lines.append("- Common top-level keys: none")

    if inventory.useful_fields:
        lines.append("- Likely useful fields:")
        for field_name in LIKELY_USEFUL_FIELDS:
            summary = inventory.useful_fields.get(field_name)
            if summary is None:
                continue

            sample_text = ", ".join(f"`{value}`" for value in summary.sample_values)
            lines.append(
                f"  - `{field_name}`: present in {summary.present_count}/{inventory.event_count} events"
                + (f". Samples: {sample_text}" if sample_text else "")
            )
    else:
        lines.append("- Likely useful fields: none extracted")

    for note in inventory.notes:
        lines.append(f"- Note: {note}")

    lines.append("")
    return lines


def main() -> int:
    args = parse_args()
    benign_dir = resolve_project_path(args.benign_dir)
    malicious_dir = resolve_project_path(args.malicious_dir)
    report_path = resolve_project_path(args.report_path)

    discovered_files: list[tuple[str, Path]] = []
    discovered_files.extend(("benign", path) for path in find_json_files(benign_dir))
    discovered_files.extend(
        ("malicious", path) for path in find_json_files(malicious_dir)
    )

    inventories = [
        inspect_file(
            path=path,
            bucket=bucket,
            top_key_limit=args.top_key_limit,
            sample_limit=args.sample_limit,
        )
        for bucket, path in discovered_files
    ]

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Scanning benign dir: {benign_dir}")
    print(f"Scanning malicious dir: {malicious_dir}")

    report = build_markdown_report(inventories)
    print(report)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(f"Saved report to {repo_relative(report_path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
