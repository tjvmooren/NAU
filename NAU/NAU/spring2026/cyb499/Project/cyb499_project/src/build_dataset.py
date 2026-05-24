from __future__ import annotations

import argparse
import csv
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

try:
    from utils import detect_json_format, flatten_windows_event, load_json_events
except ImportError:
    from src.utils import detect_json_format, flatten_windows_event, load_json_events

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RANDOM_SEED = 499
TOTAL_ROWS = 100
BENIGN_TARGET = 50
MALICIOUS_TARGET = 50

OUTPUT_COLUMNS = [
    "sample_id",
    "label",
    "source_type",
    "attack_category",
    "scenario_name",
    "source_file",
    "provider",
    "channel",
    "event_id",
    "timestamp",
    "computer",
    "user",
    "image",
    "command_line",
    "parent_image",
    "target_object",
    "destination_ip",
    "destination_hostname",
    "query_name",
    "script_block_text",
    "event_summary",
    "label_reason",
]

BENIGN_SOURCE_QUOTAS = {
    "Sysmon": 20,
    "Security": 15,
    "PowerShell": 15,
}

SAFE_BENIGN_SECURITY_EVENT_IDS = {
    "4624",
    "4672",
    "4799",
    "5024",
    "4738",
    "4648",
    "5058",
    "5061",
    "5059",
    "4798",
}

BENIGN_SUSPICIOUS_TERMS = [
    "bitsadmin",
    "invoke-webrequest",
    "xip.io",
    "directoryservices.protocols",
    "ldapconnection",
    "passwords.txt",
    "tightvnc",
    "dde_document",
    "winrar",
    "rar.exe",
    "disableregistrytools",
    "reg add",
    "foxprow.exe",
    "activatemicrosoftapp",
]

BENIGN_SYSMON_DENY_IMAGES = {
    "bitsadmin.exe",
    "chcp.com",
    "cmd.exe",
    "conhost.exe",
    "hostname.exe",
    "ping.exe",
    "powershell.exe",
    "reg.exe",
    "schtasks.exe",
    "whoami.exe",
    "wmic.exe",
}

SECONDARY_MALICIOUS_IMAGES = {
    "bitsadmin.exe",
    "chcp.com",
    "cmd.exe",
    "conhost.exe",
    "ping.exe",
    "reg.exe",
    "wmic.exe",
}

NOISE_PATTERNS = [
    "microsoftedgeupdate",
    "securityhealthservice",
    "edgeupdate",
    "mpsigstub.exe",
    "am_delta.exe",
    "microsoftedgeupdatecomregistershell64.exe",
]

ATTACK_CATEGORY_BY_FOLDER = {
    "c2c_dns_https_largequeryvolume_json": "Command and Control",
    "collection_compressData_lockwithpw_exfiltrationwinrar_json": "Collection",
    "credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json": "Credential Access",
    "defense_evasion_disable_windows_registry_tool_json": "Defense Evasion",
    "discovery_discover_system_language_withchcp_json": "Discovery",
    "execute-powershell-script-via-word-dde-json": "Execution",
    "execution-app-uninstall-using-wmic-json": "Execution",
    "lateral_powershell_lateral_usingExcelAppObject_Json": "Lateral Movement",
    "persistence_persist_download_execute_json": "Persistence",
}

SCENARIO_RULES = {
    "c2c_dns_https_largequeryvolume_json": {
        "attack_category": "Command and Control",
        "patterns": ["invoke-webrequest", "resolve?name=", "8.8.8.8", "xip.io"],
        "reason": (
            "The event shows a PowerShell-driven DNS-over-HTTPS style query loop to "
            "8.8.8.8 with randomized xip.io hostnames."
        ),
    },
    "collection_compressData_lockwithpw_exfiltrationwinrar_json": {
        "attack_category": "Collection",
        "patterns": ["winrar", "rar.exe", "hello.rar", '-hp"blue"', "victim-files"],
        "reason": (
            "The command line stages files and invokes WinRAR to create a "
            "password-protected archive."
        ),
    },
    "credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json": {
        "attack_category": "Credential Access",
        "patterns": [
            "directoryservices.protocols",
            "ldapconnection",
            "passwords.txt",
            "attempting ${password}",
            "valid credentials",
            "bruteforce",
        ],
        "reason": (
            "The PowerShell/LDAP content iterates passwords against Active Directory "
            "using System.DirectoryServices.Protocols."
        ),
    },
    "defense_evasion_disable_windows_registry_tool_json": {
        "attack_category": "Defense Evasion",
        "patterns": ["reg add", "disableregistrytools"],
        "reason": (
            "The event modifies the DisableRegistryTools policy value to restrict "
            "registry tooling."
        ),
    },
    "discovery_discover_system_language_withchcp_json": {
        "attack_category": "Discovery",
        "patterns": ['cmd.exe" /c chcp', " chcp", "chcp.com"],
        "reason": (
            "The event uses chcp to inspect the system code page, which can reveal "
            "language or locale information."
        ),
    },
    "execute-powershell-script-via-word-dde-json": {
        "attack_category": "Execution",
        "patterns": ["dde_document.docx"],
        "reason": (
            "The command starts a DDE-enabled Word document, consistent with a "
            "document-based execution chain."
        ),
    },
    "execution-app-uninstall-using-wmic-json": {
        "attack_category": "Execution",
        "patterns": ["wmic", "call uninstall", "tightvnc"],
        "reason": (
            "The event uses WMIC to uninstall a target product over WMI, which is "
            "execution behavior tied to the scenario."
        ),
    },
    "lateral_powershell_lateral_usingExcelAppObject_Json": {
        "attack_category": "Lateral Movement",
        "patterns": ["excel.application", "activatemicrosoftapp", "foxprow.exe", "calc.exe"],
        "reason": (
            "The PowerShell content copies calc.exe to a masqueraded path and "
            "instantiates an Excel COM object on localhost."
        ),
    },
    "persistence_persist_download_execute_json": {
        "attack_category": "Persistence",
        "patterns": [
            "bitsadmin",
            "/addfile",
            "/setnotifycmdline",
            "raw.githubusercontent.com",
            "bitsadmin3_flag.ps1",
        ],
        "reason": (
            "The command chain uses BITSAdmin to download content and set a notify "
            "command for follow-on execution."
        ),
    },
}


@dataclass
class EventCandidate:
    row: dict[str, str]
    score: int
    priority: str
    source_bucket: str
    group_key: str
    stable_key: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a controlled CYB 499 event-level evaluation dataset.",
    )
    parser.add_argument(
        "--benign-dir",
        type=Path,
        default=Path("data/raw/benign"),
        help="Directory containing benign raw JSON files.",
    )
    parser.add_argument(
        "--malicious-dir",
        type=Path,
        default=Path("data/raw/malicious"),
        help="Directory containing malicious-scenario raw JSON files.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("data/processed/evaluation_dataset.csv"),
        help="Output CSV path for the benchmark dataset.",
    )
    parser.add_argument(
        "--notes-path",
        type=Path,
        default=Path("report_notes/dataset_notes.md"),
        help="Output Markdown notes path.",
    )
    return parser.parse_args()


def resolve_project_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text


def collapse_whitespace(value: str) -> str:
    return " ".join(value.split())


def short_text(value: str, limit: int = 180) -> str:
    collapsed = collapse_whitespace(normalize_text(value))
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 3] + "..."


def sanitize_csv_value(value: Any) -> str:
    return normalize_text(value)


def source_type_from_channel(channel: str) -> str:
    normalized = normalize_text(channel)
    if normalized == "Microsoft-Windows-Sysmon/Operational":
        return "Sysmon"
    if normalized == "Windows PowerShell":
        return "PowerShell"
    if normalized == "Security":
        return "Security"
    if normalized == "Application":
        return "Application"
    if normalized == "System":
        return "System"
    return normalized or "Unknown"


def scenario_name_from_folder(folder_name: str) -> str:
    return re.sub(r"[_-]json$", "", folder_name, flags=re.IGNORECASE)


def iter_json_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def build_script_block_text(flat_event: dict[str, Any]) -> str:
    script_block = normalize_text(flat_event.get("ScriptBlockText"))
    if script_block:
        return script_block

    if flat_event.get("Channel") == "Windows PowerShell":
        event_data_text = normalize_text(
            flat_event.get("EventDataFields", {}).get("DataText")
        )
        return event_data_text

    return ""


def basename(path_value: str) -> str:
    if not path_value:
        return ""
    return Path(path_value).name.lower()


def build_base_row(
    *,
    label: str,
    source_file: Path,
    flat_event: dict[str, Any],
    attack_category: str = "",
    scenario_name: str = "",
) -> dict[str, str]:
    return {
        "sample_id": "",
        "label": label,
        "source_type": source_type_from_channel(normalize_text(flat_event.get("Channel"))),
        "attack_category": attack_category,
        "scenario_name": scenario_name,
        "source_file": repo_relative(source_file),
        "provider": sanitize_csv_value(flat_event.get("Provider")),
        "channel": sanitize_csv_value(flat_event.get("Channel")),
        "event_id": sanitize_csv_value(flat_event.get("EventID")),
        "timestamp": sanitize_csv_value(flat_event.get("TimeCreated")),
        "computer": sanitize_csv_value(flat_event.get("Computer")),
        "user": sanitize_csv_value(flat_event.get("User")),
        "image": sanitize_csv_value(flat_event.get("Image")),
        "command_line": sanitize_csv_value(flat_event.get("CommandLine")),
        "parent_image": sanitize_csv_value(flat_event.get("ParentImage")),
        "target_object": sanitize_csv_value(flat_event.get("TargetObject")),
        "destination_ip": sanitize_csv_value(flat_event.get("DestinationIp")),
        "destination_hostname": sanitize_csv_value(flat_event.get("DestinationHostname")),
        "query_name": sanitize_csv_value(flat_event.get("QueryName")),
        "script_block_text": sanitize_csv_value(build_script_block_text(flat_event)),
        "event_summary": "",
        "label_reason": "",
    }


def build_event_summary(
    row: dict[str, str],
    *,
    parent_command_line: str = "",
    map_description: str = "",
) -> str:
    source_type = row["source_type"] or "Unknown"
    event_id = row["event_id"] or "unknown"
    provider = row["provider"] or "unknown provider"
    computer = row["computer"] or "unknown host"
    parts = [f"{source_type} event {event_id} from {provider} on {computer}"]

    if row["image"]:
        parts.append(f"image={row['image']}")
    if row["command_line"]:
        parts.append(f"cmd={short_text(row['command_line'])}")
    elif row["script_block_text"]:
        parts.append(f"text={short_text(row['script_block_text'])}")
    if row["parent_image"]:
        parts.append(f"parent={row['parent_image']}")
    if parent_command_line:
        parts.append(f"parent_cmd={short_text(parent_command_line)}")
    if row["user"]:
        parts.append(f"user={row['user']}")
    if row["query_name"]:
        parts.append(f"query={row['query_name']}")
    if row["destination_ip"]:
        parts.append(f"dest_ip={row['destination_ip']}")
    if row["target_object"]:
        parts.append(f"target={row['target_object']}")
    if map_description:
        parts.append(f"detail={short_text(map_description, 120)}")

    return "; ".join(parts)


def benign_group_key(row: dict[str, str]) -> str:
    source_type = row["source_type"]
    if source_type == "PowerShell":
        return f"{row['event_id']}|{short_text(row['command_line'], 80)}"
    if source_type == "Security":
        return row["event_id"] or "unknown"
    if source_type == "Sysmon":
        return basename(row["image"]) or "unknown"
    return row["source_file"]


def benign_score(row: dict[str, str]) -> int:
    score = 0
    command_line = row["command_line"].lower()
    image_name = basename(row["image"])

    if row["source_type"] == "PowerShell":
        score += 5
        if "get-service" in command_line or "get-process" in command_line:
            score += 3
        if "write-host" in command_line:
            score += 2
        if row["event_id"] in {"400", "403", "600"}:
            score += 1

    if row["source_type"] == "Security":
        score += 5
        if row["event_id"] in {"4624", "4672", "4799", "4798"}:
            score += 2

    if row["source_type"] == "Sysmon":
        score += 4
        if image_name in {
            "wuauclt.exe",
            "msiexec.exe",
            "runtimebroker.exe",
            "trustedinstaller.exe",
            "tiworker.exe",
            "wermgr.exe",
            "svchost.exe",
            "backgroundtaskhost.exe",
            "windowspackagemanagerserver.exe",
            "securebootencodeuefi.exe",
            "msedge.exe",
            "microsoftedgeupdate.exe",
        }:
            score += 3
        if row["event_id"] == "1":
            score += 1

    return score


def is_benign_candidate(row: dict[str, str]) -> bool:
    source_type = row["source_type"]
    searchable = " ".join(
        [
            row["image"],
            row["command_line"],
            row["parent_image"],
            row["script_block_text"],
        ]
    ).lower()

    if any(term in searchable for term in BENIGN_SUSPICIOUS_TERMS):
        return False

    if source_type == "PowerShell":
        return row["event_id"] in {"400", "403", "600"}

    if source_type == "Security":
        return row["event_id"] in SAFE_BENIGN_SECURITY_EVENT_IDS

    if source_type == "Sysmon":
        image_name = basename(row["image"])
        if image_name in BENIGN_SYSMON_DENY_IMAGES:
            return False
        if " /delete " in searchable or " /create " in searchable:
            return False
        if " rd /s /q " in searchable:
            return False
        return row["event_id"] in {"1", "5", "4"}

    return False


def build_benign_reason(row: dict[str, str]) -> str:
    if row["source_type"] == "PowerShell":
        return (
            "Selected from the benign baseline PowerShell log; the host application "
            "shows routine shell startup or administrative commands without attack-specific indicators."
        )
    if row["source_type"] == "Security":
        return (
            "Selected from the benign baseline Security log; this is routine Windows "
            "audit activity rather than an attack-specific event."
        )
    if row["source_type"] == "Sysmon":
        return (
            "Selected from the benign baseline Sysmon log; the process activity is "
            "routine system or application behavior without the malicious-side patterns."
        )
    return "Selected from the benign baseline source data."


def contains_noise(text: str) -> bool:
    return any(pattern in text for pattern in NOISE_PATTERNS)


def build_evidence_snippet(row: dict[str, str], parent_command_line: str) -> str:
    for value in (
        row["command_line"],
        row["script_block_text"],
        row["target_object"],
        row["query_name"],
        row["destination_ip"],
        parent_command_line,
    ):
        if value:
            return short_text(value, 220)
    return short_text(row["image"], 220)


def build_secondary_reason(parent_command_line: str) -> str:
    return (
        "This event is retained because its parent command line carries the same "
        f"attack evidence: {short_text(parent_command_line, 220)}"
    )


def evaluate_malicious_candidate(
    row: dict[str, str],
    *,
    scenario_folder: str,
    event_data_text: str,
    parent_command_line: str,
) -> tuple[int, str, str] | None:
    meta = SCENARIO_RULES.get(scenario_folder)
    if meta is None:
        return None

    direct_text = " || ".join(
        value.lower()
        for value in [
            row["image"],
            row["command_line"],
            row["parent_image"],
            row["target_object"],
            row["destination_ip"],
            row["destination_hostname"],
            row["query_name"],
            row["script_block_text"],
            event_data_text,
        ]
        if value
    )
    parent_text = parent_command_line.lower()
    image_name = basename(row["image"])
    patterns = meta["patterns"]

    direct_hits = [pattern for pattern in patterns if pattern in direct_text]
    parent_hits = [pattern for pattern in patterns if pattern in parent_text]

    if direct_hits:
        score = 10 + len(direct_hits)
        if row["source_type"] == "PowerShell":
            score += 2
        if row["source_type"] == "Sysmon":
            score += 1
        if contains_noise(direct_text):
            score -= 3
        reason = f"{meta['reason']} Evidence: {build_evidence_snippet(row, parent_command_line)}"
        return score, "primary", reason

    if parent_hits and image_name in SECONDARY_MALICIOUS_IMAGES:
        score = 4
        if image_name in {"bitsadmin.exe", "wmic.exe", "reg.exe", "ping.exe", "chcp.com"}:
            score += 2
        reason = build_secondary_reason(parent_command_line)
        return score, "secondary", reason

    return None


def stable_row_key(path: Path, index: int, row: dict[str, str]) -> str:
    pieces = [
        repo_relative(path),
        str(index),
        row["event_id"],
        row["timestamp"],
        row["image"],
        row["command_line"],
    ]
    return "||".join(pieces)


def round_robin_select(
    candidates: list[EventCandidate],
    target: int,
    group_key_fn: Callable[[EventCandidate], str],
) -> list[EventCandidate]:
    grouped: dict[str, list[EventCandidate]] = defaultdict(list)
    for candidate in candidates:
        grouped[group_key_fn(candidate)].append(candidate)

    ordered_groups = sorted(grouped)
    selected: list[EventCandidate] = []

    while len(selected) < target:
        progress = False
        for group in ordered_groups:
            bucket = grouped[group]
            if not bucket:
                continue
            selected.append(bucket.pop(0))
            progress = True
            if len(selected) == target:
                break
        if not progress:
            break

    return selected


def select_benign_events(benign_dir: Path) -> list[EventCandidate]:
    candidates_by_source: dict[str, list[EventCandidate]] = defaultdict(list)

    for path in iter_json_files(benign_dir):
        format_name = detect_json_format(path)
        if format_name == "empty":
            continue

        for index, event in enumerate(load_json_events(path, format_name)):
            if not isinstance(event, dict):
                continue

            flat_event = flatten_windows_event(event)
            row = build_base_row(
                label="Benign",
                source_file=path,
                flat_event=flat_event,
                scenario_name=path.stem,
            )

            if not is_benign_candidate(row):
                continue

            parent_command_line = normalize_text(
                flat_event.get("EventDataFields", {}).get("ParentCommandLine")
            )
            map_description = normalize_text(flat_event.get("MapDescription"))
            row["event_summary"] = build_event_summary(
                row,
                parent_command_line=parent_command_line,
                map_description=map_description,
            )
            row["label_reason"] = build_benign_reason(row)

            candidate = EventCandidate(
                row=row,
                score=benign_score(row),
                priority="primary",
                source_bucket=row["source_type"],
                group_key=benign_group_key(row),
                stable_key=stable_row_key(path, index, row),
            )
            candidates_by_source[row["source_type"]].append(candidate)

    selected: list[EventCandidate] = []

    for source_type, quota in BENIGN_SOURCE_QUOTAS.items():
        source_candidates = sorted(
            candidates_by_source[source_type],
            key=lambda item: (-item.score, item.group_key, item.stable_key),
        )
        chosen = round_robin_select(source_candidates, quota, lambda item: item.group_key)
        if len(chosen) < quota:
            raise ValueError(
                f"Only found {len(chosen)} benign {source_type} events, but quota is {quota}."
            )
        selected.extend(chosen)

    if len(selected) != BENIGN_TARGET:
        raise ValueError(f"Expected {BENIGN_TARGET} benign rows, got {len(selected)}.")

    return selected


def select_malicious_events(malicious_dir: Path) -> list[EventCandidate]:
    primary_candidates: list[EventCandidate] = []
    secondary_candidates: list[EventCandidate] = []

    for path in iter_json_files(malicious_dir):
        format_name = detect_json_format(path)
        if format_name == "empty":
            continue

        scenario_folder = path.parent.name
        attack_category = ATTACK_CATEGORY_BY_FOLDER.get(scenario_folder, "")
        scenario_name = scenario_name_from_folder(scenario_folder)

        for index, event in enumerate(load_json_events(path, format_name)):
            if not isinstance(event, dict):
                continue

            flat_event = flatten_windows_event(event)
            row = build_base_row(
                label="Malicious",
                source_file=path,
                flat_event=flat_event,
                attack_category=attack_category,
                scenario_name=scenario_name,
            )

            event_data_fields = flat_event.get("EventDataFields", {})
            event_data_text = normalize_text(event_data_fields.get("DataText"))
            parent_command_line = normalize_text(event_data_fields.get("ParentCommandLine"))
            map_description = normalize_text(flat_event.get("MapDescription"))

            evaluation = evaluate_malicious_candidate(
                row,
                scenario_folder=scenario_folder,
                event_data_text=event_data_text,
                parent_command_line=parent_command_line,
            )
            if evaluation is None:
                continue

            score, priority, reason = evaluation
            row["event_summary"] = build_event_summary(
                row,
                parent_command_line=parent_command_line,
                map_description=map_description,
            )
            row["label_reason"] = reason

            candidate = EventCandidate(
                row=row,
                score=score,
                priority=priority,
                source_bucket=scenario_name,
                group_key=scenario_name,
                stable_key=stable_row_key(path, index, row),
            )

            if priority == "primary":
                primary_candidates.append(candidate)
            else:
                secondary_candidates.append(candidate)

    primary_candidates.sort(key=lambda item: (-item.score, item.group_key, item.stable_key))
    secondary_candidates.sort(key=lambda item: (-item.score, item.group_key, item.stable_key))

    if len(primary_candidates) >= MALICIOUS_TARGET:
        selected = round_robin_select(
            primary_candidates,
            MALICIOUS_TARGET,
            lambda item: item.group_key,
        )
    else:
        selected = list(primary_candidates)
        remaining = MALICIOUS_TARGET - len(selected)
        fill = round_robin_select(
            secondary_candidates,
            remaining,
            lambda item: item.group_key,
        )
        selected.extend(fill)

    if len(selected) != MALICIOUS_TARGET:
        raise ValueError(
            f"Expected {MALICIOUS_TARGET} malicious rows, got {len(selected)}. "
            "Adjust the malicious selection rules or targets."
        )

    return selected


def assign_sample_ids(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    for index, row in enumerate(rows, start=1):
        row["sample_id"] = f"CYB499-{index:03d}"
    return rows


def write_csv(output_path: Path, rows: list[dict[str, str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def counter_lines(counter: Counter[str]) -> list[str]:
    lines: list[str] = []
    for key, value in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{key}`: {value}")
    return lines


def build_dataset_notes(
    *,
    benign_dir: Path,
    malicious_dir: Path,
    output_csv: Path,
    rows: list[dict[str, str]],
) -> str:
    benign_files = iter_json_files(benign_dir)
    malicious_files = iter_json_files(malicious_dir)
    non_empty_malicious_files = [
        path for path in malicious_files if detect_json_format(path) != "empty"
    ]

    label_counts = Counter(row["label"] for row in rows)
    source_file_counts = Counter(row["source_file"] for row in rows)
    scenario_counts = Counter(
        row["scenario_name"] for row in rows if row["label"] == "Malicious"
    )
    label_source_counts = Counter(f"{row['label']} / {row['source_type']}" for row in rows)

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

    lines = [
        "# Dataset Notes",
        "",
        f"Generated: `{generated_at}`",
        f"Seed: `{RANDOM_SEED}`",
        "",
        "## Raw File Counts",
        "",
        f"- Benign JSON files scanned: {len(benign_files)}",
        f"- Malicious JSON files scanned: {len(malicious_files)}",
        f"- Non-empty malicious JSON files scanned: {len(non_empty_malicious_files)}",
        "",
        "## Selected Row Counts",
        "",
        f"- Total rows: {len(rows)}",
        f"- Benign rows: {label_counts.get('Benign', 0)}",
        f"- Malicious rows: {label_counts.get('Malicious', 0)}",
        "",
        "### By Label / Source Type",
        "",
        *counter_lines(label_source_counts),
        "",
        "### By Scenario (Malicious Only)",
        "",
        *counter_lines(scenario_counts),
        "",
        "### By Source File",
        "",
        *counter_lines(source_file_counts),
        "",
        "## Label Logic",
        "",
        "- Benign rows are sampled only from `data/raw/benign` and are filtered toward routine Sysmon, Security, and PowerShell telemetry.",
        "- Benign rows exclude the attack-specific keywords that drive malicious selection, so the benchmark does not label obvious attack-pattern strings as benign.",
        "- Malicious rows are selected event by event. The script does not label an entire attack-scenario folder as malicious by default.",
        "- Malicious selection requires direct attack evidence in the event itself or in a preserved `ParentCommandLine` field for a child event in the same execution chain.",
        "- High-priority malicious evidence includes suspicious PowerShell content, `reg add` policy changes, `wmic` uninstall commands, `bitsadmin` download-and-notify chains, `WinRAR` archive creation, `chcp` discovery, DDE document launch, and Excel COM / copy-based lateral movement behavior.",
        "- Background noise such as Microsoft Edge update activity and `SecurityHealthService.exe` is intentionally excluded unless a row also carries explicit attack evidence.",
        "",
        "## Limitations",
        "",
        "- This repository's benign side contains Sysmon, Security, and Windows PowerShell logs only; there are no benign Application or System JSON files to sample from.",
        "- Some malicious PowerShell rows use normalized `EventData` text as `script_block_text` because the raw export does not always expose a dedicated `ScriptBlockText` field.",
        "- Several malicious PowerShell rows come from different telemetry points around the same command, because the available event-level evidence is limited and the dataset target is fixed at 50 malicious rows.",
        "- The benchmark is conservative by design: it aims to keep only events with explicit attack-relevant context rather than maximizing coverage of every scenario event.",
        "",
        "## Output",
        "",
        f"- Dataset CSV: `{repo_relative(output_csv)}`",
    ]

    return "\n".join(lines) + "\n"


def print_final_summary(rows: list[dict[str, str]], output_csv: Path, notes_path: Path) -> None:
    label_counts = Counter(row["label"] for row in rows)
    source_counts = Counter(row["source_type"] for row in rows)

    print(f"Saved dataset to {repo_relative(output_csv)}")
    print(f"Saved notes to {repo_relative(notes_path)}")
    print("Label counts:")
    for label, count in sorted(label_counts.items()):
        print(f"  {label}: {count}")
    print("Source counts:")
    for source_type, count in sorted(source_counts.items()):
        print(f"  {source_type}: {count}")


def main() -> int:
    args = parse_args()
    benign_dir = resolve_project_path(args.benign_dir)
    malicious_dir = resolve_project_path(args.malicious_dir)
    output_csv = resolve_project_path(args.output_csv)
    notes_path = resolve_project_path(args.notes_path)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Benign dir: {benign_dir}")
    print(f"Malicious dir: {malicious_dir}")
    print(f"Random seed: {RANDOM_SEED}")

    benign_rows = [candidate.row for candidate in select_benign_events(benign_dir)]
    malicious_rows = [candidate.row for candidate in select_malicious_events(malicious_dir)]

    if len(benign_rows) != BENIGN_TARGET or len(malicious_rows) != MALICIOUS_TARGET:
        raise ValueError(
            f"Expected {BENIGN_TARGET} benign and {MALICIOUS_TARGET} malicious rows, "
            f"got {len(benign_rows)} and {len(malicious_rows)}."
        )

    all_rows = benign_rows + malicious_rows
    rng = random.Random(RANDOM_SEED)
    rng.shuffle(all_rows)
    assign_sample_ids(all_rows)

    if len(all_rows) != TOTAL_ROWS:
        raise ValueError(f"Expected {TOTAL_ROWS} total rows, got {len(all_rows)}.")

    write_csv(output_csv, all_rows)

    notes = build_dataset_notes(
        benign_dir=benign_dir,
        malicious_dir=malicious_dir,
        output_csv=output_csv,
        rows=all_rows,
    )
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(notes, encoding="utf-8")

    print_final_summary(all_rows, output_csv, notes_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
