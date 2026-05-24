from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gpt-5.4"
VALID_CLASSIFICATIONS = {"Malicious", "Benign"}
VALID_CONFIDENCE = {"High", "Medium", "Low"}
DEFAULT_MAX_OUTPUT_TOKENS = 300

EVENT_FIELDS = [
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
]

OUTPUT_COLUMNS = [
    "sample_id",
    "ground_truth",
    "prediction",
    "confidence",
    "evidence",
    "key_fields",
    "raw_response",
    "model",
    "prompt_name",
    "status",
    "error_message",
]


@dataclass(frozen=True)
class PromptConfig:
    name: str
    prompt_path: Path
    output_path: Path
    schema_name: str
    schema: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run OpenAI classification evaluation on the CYB 499 dataset.",
    )
    parser.add_argument(
        "--dataset-path",
        type=Path,
        default=Path("data/processed/evaluation_dataset.csv"),
        help="Path to the evaluation dataset CSV.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="OpenAI model name to use for evaluation.",
    )
    parser.add_argument(
        "--prompt-mode",
        choices=["direct", "structured", "both"],
        default="both",
        help="Which prompt configuration to run.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional limit for the number of dataset rows to process.",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=DEFAULT_MAX_OUTPUT_TOKENS,
        help="Maximum response tokens per request.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore completed rows and recompute the selected output files from scratch.",
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
    return str(value).strip()


def load_env_file() -> None:
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(PROJECT_ROOT / ".env")
        return
    except ImportError:
        pass

    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_dataset_rows(dataset_path: Path, max_rows: int | None = None) -> list[dict[str, str]]:
    with dataset_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [{normalize_text(key): normalize_text(value) for key, value in row.items()} for row in reader]

    required_columns = {"sample_id", "label"}
    if rows:
        missing = sorted(column for column in required_columns if column not in rows[0])
        if missing:
            raise ValueError(
                f"Dataset is missing required column(s): {missing}. "
                "Expected at least `sample_id` and `label`."
            )

    if max_rows is not None:
        return rows[:max_rows]
    return rows


def load_prompt_text(prompt_path: Path) -> str:
    return prompt_path.read_text(encoding="utf-8").strip()


def build_prompt_configs() -> dict[str, PromptConfig]:
    direct_schema = {
        "type": "object",
        "properties": {
            "classification": {
                "type": "string",
                "enum": ["Malicious", "Benign"],
            },
            "confidence": {
                "type": "string",
                "enum": ["High", "Medium", "Low"],
            },
            "evidence": {"type": "string"},
        },
        "required": ["classification", "confidence", "evidence"],
        "additionalProperties": False,
    }
    structured_schema = {
        "type": "object",
        "properties": {
            "classification": {
                "type": "string",
                "enum": ["Malicious", "Benign"],
            },
            "confidence": {
                "type": "string",
                "enum": ["High", "Medium", "Low"],
            },
            "key_fields": {
                "type": "array",
                "items": {"type": "string"},
            },
            "evidence": {"type": "string"},
        },
        "required": ["classification", "confidence", "key_fields", "evidence"],
        "additionalProperties": False,
    }

    return {
        "direct": PromptConfig(
            name="direct",
            prompt_path=resolve_project_path(Path("prompts/direct_prompt.txt")),
            output_path=resolve_project_path(Path("results/raw_model_outputs/openai_direct.csv")),
            schema_name="cyb499_direct_classification",
            schema=direct_schema,
        ),
        "structured": PromptConfig(
            name="structured",
            prompt_path=resolve_project_path(Path("prompts/structured_reasoning_prompt.txt")),
            output_path=resolve_project_path(Path("results/raw_model_outputs/openai_structured.csv")),
            schema_name="cyb499_structured_classification",
            schema=structured_schema,
        ),
    }


def build_event_payload(row: dict[str, str]) -> dict[str, str]:
    payload: dict[str, str] = {}
    for field in EVENT_FIELDS:
        value = normalize_text(row.get(field, ""))
        if value:
            payload[field] = value
    return payload


def build_user_input(row: dict[str, str]) -> str:
    payload = build_event_payload(row)
    return (
        "Classify this single Windows Event Log event using only the supplied fields.\n"
        "Event fields (JSON):\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=False)}"
    )


def load_existing_results(output_path: Path) -> dict[str, dict[str, str]]:
    if not output_path.exists():
        return {}

    with output_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            normalized = {
                normalize_text(key): normalize_text(value)
                for key, value in row.items()
                if key is not None
            }
            sample_id = normalized.get("sample_id", "")
            if sample_id:
                rows[sample_id] = normalized
        return rows


def is_completed_result(row: dict[str, str], model: str, prompt_name: str) -> bool:
    if row.get("status") != "completed":
        return False
    if row.get("model") and row.get("model") != model:
        return False
    if row.get("prompt_name") and row.get("prompt_name") != prompt_name:
        return False
    if row.get("prediction") not in VALID_CLASSIFICATIONS:
        return False
    if row.get("confidence") not in VALID_CONFIDENCE:
        return False
    return True


def validate_existing_results(
    existing_rows: dict[str, dict[str, str]],
    *,
    model: str,
    prompt_name: str,
    force: bool,
) -> None:
    if force or not existing_rows:
        return

    conflicting_models = {
        row.get("model", "")
        for row in existing_rows.values()
        if row.get("status") == "completed" and row.get("model") and row.get("model") != model
    }
    if conflicting_models:
        raise ValueError(
            f"{prompt_name} results already contain completed rows for other model(s): "
            f"{sorted(conflicting_models)}. Re-run with --force to overwrite them."
        )


def parse_response_payload(raw_response: str) -> dict[str, Any]:
    if not raw_response:
        return {}
    return json.loads(raw_response)


def extract_output_text(response: Any) -> str:
    direct_text = normalize_text(getattr(response, "output_text", ""))
    if direct_text:
        return direct_text

    model_dump = getattr(response, "model_dump", None)
    if not callable(model_dump):
        return ""

    payload = model_dump()
    output_items = payload.get("output", [])
    fragments: list[str] = []
    for item in output_items:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            text_value = normalize_text(content.get("text", ""))
            if text_value:
                fragments.append(text_value)

    return "\n".join(fragment for fragment in fragments if fragment).strip()


def build_response_text_config(config: PromptConfig) -> dict[str, Any]:
    return {
        "format": {
            "type": "json_schema",
            "name": config.schema_name,
            "schema": config.schema,
            "strict": True,
        }
    }


def call_openai_for_row(
    *,
    client: OpenAI,
    model: str,
    prompt_text: str,
    prompt_config: PromptConfig,
    row: dict[str, str],
    max_output_tokens: int,
) -> tuple[dict[str, Any], str]:
    response = client.responses.create(
        model=model,
        instructions=prompt_text,
        input=build_user_input(row),
        temperature=0,
        max_output_tokens=max_output_tokens,
        text=build_response_text_config(prompt_config),
        user=row["sample_id"],
    )

    raw_response = extract_output_text(response)
    if not raw_response and hasattr(response, "model_dump_json"):
        raw_response = response.model_dump_json(indent=2)

    parsed = parse_response_payload(raw_response)
    return parsed, raw_response


def build_result_row(
    *,
    dataset_row: dict[str, str],
    prompt_name: str,
    model: str,
    parsed_response: dict[str, Any] | None,
    raw_response: str,
    error_message: str = "",
) -> dict[str, str]:
    prediction = normalize_text((parsed_response or {}).get("classification", ""))
    confidence = normalize_text((parsed_response or {}).get("confidence", ""))
    evidence = normalize_text((parsed_response or {}).get("evidence", ""))
    key_fields_value = (parsed_response or {}).get("key_fields", [])

    if isinstance(key_fields_value, list):
        key_fields = json.dumps(key_fields_value, ensure_ascii=False)
    else:
        key_fields = ""

    status = "completed"
    if prediction not in VALID_CLASSIFICATIONS or confidence not in VALID_CONFIDENCE:
        status = "error"
        if not error_message:
            error_message = "Model response did not match the expected classification/confidence schema."

    return {
        "sample_id": dataset_row["sample_id"],
        "ground_truth": dataset_row["label"],
        "prediction": prediction,
        "confidence": confidence,
        "evidence": evidence,
        "key_fields": key_fields,
        "raw_response": raw_response,
        "model": model,
        "prompt_name": prompt_name,
        "status": status,
        "error_message": error_message,
    }


def write_results(
    *,
    output_path: Path,
    dataset_rows: list[dict[str, str]],
    results_by_sample_id: dict[str, dict[str, str]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for dataset_row in dataset_rows:
            sample_id = dataset_row["sample_id"]
            if sample_id in results_by_sample_id:
                writer.writerow(results_by_sample_id[sample_id])


def run_prompt_evaluation(
    *,
    client: OpenAI,
    dataset_rows: list[dict[str, str]],
    prompt_config: PromptConfig,
    model: str,
    max_output_tokens: int,
    force: bool,
) -> None:
    prompt_text = load_prompt_text(prompt_config.prompt_path)
    existing_rows = {} if force else load_existing_results(prompt_config.output_path)
    validate_existing_results(
        existing_rows,
        model=model,
        prompt_name=prompt_config.name,
        force=force,
    )

    completed_count = 0
    for existing_row in existing_rows.values():
        if is_completed_result(existing_row, model, prompt_config.name):
            completed_count += 1

    print(
        f"[{prompt_config.name}] output={repo_relative(prompt_config.output_path)} "
        f"existing_completed={completed_count}"
    )

    total_rows = len(dataset_rows)
    for index, dataset_row in enumerate(dataset_rows, start=1):
        sample_id = dataset_row["sample_id"]
        existing_row = existing_rows.get(sample_id)

        if existing_row and is_completed_result(existing_row, model, prompt_config.name):
            continue

        try:
            parsed_response, raw_response = call_openai_for_row(
                client=client,
                model=model,
                prompt_text=prompt_text,
                prompt_config=prompt_config,
                row=dataset_row,
                max_output_tokens=max_output_tokens,
            )
            result_row = build_result_row(
                dataset_row=dataset_row,
                prompt_name=prompt_config.name,
                model=model,
                parsed_response=parsed_response,
                raw_response=raw_response,
            )
        except Exception as exc:
            result_row = build_result_row(
                dataset_row=dataset_row,
                prompt_name=prompt_config.name,
                model=model,
                parsed_response=None,
                raw_response="",
                error_message=str(exc),
            )

        existing_rows[sample_id] = result_row
        write_results(
            output_path=prompt_config.output_path,
            dataset_rows=dataset_rows,
            results_by_sample_id=existing_rows,
        )

        print(
            f"[{prompt_config.name}] {index}/{total_rows} sample_id={sample_id} "
            f"status={result_row['status']} prediction={result_row['prediction'] or 'N/A'}"
        )


def main() -> int:
    args = parse_args()
    load_env_file()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. Add it to your environment or to a .env file "
            "at the project root."
        )

    dataset_path = resolve_project_path(args.dataset_path)
    dataset_rows = load_dataset_rows(dataset_path, max_rows=args.max_rows)
    prompt_configs = build_prompt_configs()

    selected_configs: list[PromptConfig]
    if args.prompt_mode == "both":
        selected_configs = [prompt_configs["direct"], prompt_configs["structured"]]
    else:
        selected_configs = [prompt_configs[args.prompt_mode]]

    client = OpenAI(api_key=api_key)

    print(f"Dataset: {repo_relative(dataset_path)}")
    print(f"Rows to process: {len(dataset_rows)}")
    print(f"Model: {args.model}")
    print(f"Prompt mode: {args.prompt_mode}")

    for prompt_config in selected_configs:
        run_prompt_evaluation(
            client=client,
            dataset_rows=dataset_rows,
            prompt_config=prompt_config,
            model=args.model,
            max_output_tokens=args.max_output_tokens,
            force=args.force,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
