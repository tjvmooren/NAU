from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from run_openai_eval import (
    PromptConfig,
    build_result_row,
    build_user_input,
    is_completed_result,
    load_dataset_rows,
    load_env_file,
    load_existing_results,
    load_prompt_text,
    normalize_text,
    repo_relative,
    resolve_project_path,
    validate_existing_results,
    write_results,
)

DEFAULT_MODEL = "Qwen/Qwen3-4B-Instruct-2507"
DEFAULT_MAX_NEW_TOKENS = 160


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run local Qwen evaluation on the CYB 499 dataset using Hugging Face Transformers.",
    )
    parser.add_argument(
        "--dataset-path",
        type=Path,
        default=Path("data/processed/evaluation_dataset.csv"),
        help="Path to the evaluation dataset CSV.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("QWEN_MODEL") or DEFAULT_MODEL,
        help="Transformers model name to load. Defaults to Qwen/Qwen3-4B-Instruct-2507.",
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
        "--max-new-tokens",
        type=int,
        default=DEFAULT_MAX_NEW_TOKENS,
        help="Maximum generated tokens per response. Keep this small because the output should be strict JSON.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore completed rows and recompute the selected output files from scratch.",
    )
    return parser.parse_args()


def get_hf_token() -> str:
    return (
        os.getenv("huggfaceapi")
        or os.getenv("HF_TOKEN")
        or os.getenv("HUGGINGFACE_API_KEY")
        or ""
    )


def build_prompt_configs() -> dict[str, PromptConfig]:
    empty_schema: dict[str, Any] = {}
    return {
        "direct": PromptConfig(
            name="direct",
            prompt_path=resolve_project_path(Path("prompts/direct_prompt.txt")),
            output_path=resolve_project_path(Path("results/raw_model_outputs/qwen_direct.csv")),
            schema_name="",
            schema=empty_schema,
        ),
        "structured": PromptConfig(
            name="structured",
            prompt_path=resolve_project_path(Path("prompts/structured_reasoning_prompt.txt")),
            output_path=resolve_project_path(Path("results/raw_model_outputs/qwen_structured.csv")),
            schema_name="",
            schema=empty_schema,
        ),
    }


def build_fallback_prompt(prompt_text: str, row: dict[str, str]) -> str:
    return (
        f"{prompt_text}\n\n"
        f"{build_user_input(row)}\n\n"
        "Return strict JSON only.\n"
    )


def extract_json_candidates(text: str) -> list[str]:
    stripped = normalize_text(text)
    if not stripped:
        return []

    candidates = [stripped]
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3:
            fenced_body = "\n".join(lines[1:-1]).strip()
            if fenced_body:
                candidates.append(fenced_body)

    first_brace = stripped.find("{")
    last_brace = stripped.rfind("}")
    if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
        candidates.append(stripped[first_brace : last_brace + 1])

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            deduped.append(candidate)
    return deduped


def parse_response_payload(raw_response: str) -> dict[str, Any]:
    for candidate in extract_json_candidates(raw_response):
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return {}


class QwenModelRunner:
    def __init__(self, model_name: str, hf_token: str) -> None:
        token = normalize_text(hf_token) or None
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading local transformers model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
        self.model.eval()

        if self.tokenizer.pad_token is None and self.tokenizer.eos_token is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model.to(self.device)

    def build_generation_prompt(self, prompt_text: str, row: dict[str, str]) -> str:
        if hasattr(self.tokenizer, "apply_chat_template"):
            messages = [
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": build_user_input(row)},
            ]
            try:
                return self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
            except Exception:
                pass

        return build_fallback_prompt(prompt_text, row)

    def run(self, prompt_text: str, row: dict[str, str], max_new_tokens: int) -> str:
        prompt = self.build_generation_prompt(prompt_text, row)
        encoded_input = self.tokenizer(prompt, return_tensors="pt")
        encoded_input = {key: value.to(self.device) for key, value in encoded_input.items()}

        pad_token_id = self.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.tokenizer.eos_token_id

        with torch.no_grad():
            output = self.model.generate(
                **encoded_input,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                num_beams=1,
                pad_token_id=pad_token_id,
            )

        prompt_length = encoded_input["input_ids"].shape[1]
        generated_ids = output[0][prompt_length:]
        generated_text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return generated_text.strip()


def run_prompt_evaluation(
    *,
    dataset_rows: list[dict[str, str]],
    prompt_config: PromptConfig,
    model: str,
    max_new_tokens: int,
    force: bool,
    model_runner: QwenModelRunner | None,
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
            if model_runner is None:
                raise RuntimeError("Qwen model runner was not initialized.")

            raw_response = model_runner.run(
                prompt_text=prompt_text,
                row=dataset_row,
                max_new_tokens=max_new_tokens,
            )
            parsed_response = parse_response_payload(raw_response)
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
    load_env_file()
    args = parse_args()
    torch.manual_seed(0)

    dataset_path = resolve_project_path(args.dataset_path)
    dataset_rows = load_dataset_rows(dataset_path, max_rows=args.max_rows)
    prompt_configs = build_prompt_configs()

    selected_configs: list[PromptConfig]
    if args.prompt_mode == "both":
        selected_configs = [prompt_configs["direct"], prompt_configs["structured"]]
    else:
        selected_configs = [prompt_configs[args.prompt_mode]]

    print(f"Dataset: {repo_relative(dataset_path)}")
    print(f"Rows to process: {len(dataset_rows)}")
    print(f"Model: {args.model}")
    print("Backend: local transformers")
    print(f"Prompt mode: {args.prompt_mode}")

    model_runner: QwenModelRunner | None = None
    if args.max_rows != 0:
        model_runner = QwenModelRunner(args.model, get_hf_token())

    for prompt_config in selected_configs:
        run_prompt_evaluation(
            dataset_rows=dataset_rows,
            prompt_config=prompt_config,
            model=args.model,
            max_new_tokens=args.max_new_tokens,
            force=args.force,
            model_runner=model_runner,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
