from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from run_openai_eval import (
    DEFAULT_MAX_OUTPUT_TOKENS,
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

DEFAULT_MODEL_FALLBACK = "meta-llama/llama-3.2-1B"
DEFAULT_API_KEY_FALLBACK = os.getenv("huggfaceapi")


def get_default_model() -> str:
    return os.getenv("HF_MODEL") or os.getenv("LLAMA_MODEL") or DEFAULT_MODEL_FALLBACK


def get_default_base_url() -> str:
    return os.getenv("HF_BASE_URL") or os.getenv("LLAMA_BASE_URL") or ""


def get_default_api_key() -> str:
    return (
        os.getenv("huggfaceapi")
        or os.getenv("HF_TOKEN")
        or os.getenv("HUGGINGFACE_API_KEY")
        or os.getenv("LLAMA_API_KEY")
        or DEFAULT_API_KEY_FALLBACK
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run local Hugging Face or compatible endpoint evaluation on the CYB 499 dataset.",
    )
    parser.add_argument(
        "--dataset-path",
        type=Path,
        default=Path("data/processed/evaluation_dataset.csv"),
        help="Path to the evaluation dataset CSV.",
    )
    parser.add_argument(
        "--model",
        default=get_default_model(),
        help="Model name. Defaults to HF_MODEL, then LLAMA_MODEL.",
    )
    parser.add_argument(
        "--base-url",
        default=get_default_base_url(),
        help="Optional OpenAI-compatible endpoint base URL. Leave unset to run locally with transformers.",
    )
    parser.add_argument(
        "--api-key",
        default=get_default_api_key(),
        help="API key or Hugging Face token. Defaults to huggfaceapi, HF_TOKEN, HUGGINGFACE_API_KEY, then LLAMA_API_KEY.",
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
        help="Maximum generated tokens per response.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore completed rows and recompute the selected output files from scratch.",
    )
    return parser.parse_args()


def build_prompt_configs() -> dict[str, PromptConfig]:
    empty_schema: dict[str, Any] = {}
    return {
        "direct": PromptConfig(
            name="direct",
            prompt_path=resolve_project_path(Path("prompts/direct_prompt.txt")),
            output_path=resolve_project_path(Path("results/raw_model_outputs/llama_direct.csv")),
            schema_name="",
            schema=empty_schema,
        ),
        "structured": PromptConfig(
            name="structured",
            prompt_path=resolve_project_path(Path("prompts/structured_reasoning_prompt.txt")),
            output_path=resolve_project_path(Path("results/raw_model_outputs/llama_structured.csv")),
            schema_name="",
            schema=empty_schema,
        ),
    }


def normalize_base_url(base_url: str) -> str:
    return normalize_text(base_url).rstrip("/")


def uses_local_transformers_mode(base_url: str) -> bool:
    return normalize_base_url(base_url) == ""


def is_ollama_endpoint(base_url: str) -> bool:
    lowered = normalize_base_url(base_url).lower()
    return "ollama" in lowered or ":11434" in lowered


def build_local_generation_prompt(prompt_text: str, row: dict[str, str]) -> str:
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


class LocalHFModelRunner:
    def __init__(self, model_name: str, api_key: str) -> None:
        token = normalize_text(api_key) or None
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading local transformers model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
        self.model.eval()

        if self.tokenizer.pad_token is None and self.tokenizer.eos_token is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model.to(self.device)

    def run(self, prompt: str, max_new_tokens: int) -> str:
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
                pad_token_id=pad_token_id,
            )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        prompt_text = self.tokenizer.decode(
            encoded_input["input_ids"][0],
            skip_special_tokens=True,
        )

        if generated_text.startswith(prompt_text):
            generated_text = generated_text[len(prompt_text) :]

        return generated_text.strip()


class EndpointModelRunner:
    def __init__(self, model_name: str, base_url: str, api_key: str) -> None:
        self.model_name = model_name
        self.base_url = normalize_base_url(base_url)
        self.api_key = normalize_text(api_key)

    def _chat_completions_url(self) -> str:
        if self.base_url.endswith("/chat/completions"):
            return self.base_url
        return f"{self.base_url}/chat/completions"

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _payload(
        self,
        *,
        prompt_text: str,
        row: dict[str, str],
        max_output_tokens: int,
        use_json_mode: bool,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": build_user_input(row)},
            ],
            "temperature": 0,
            "max_tokens": max_output_tokens,
        }

        if use_json_mode:
            if is_ollama_endpoint(self.base_url):
                payload["format"] = "json"
            else:
                payload["response_format"] = {"type": "json_object"}

        return payload

    def _post_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = urllib_request.Request(
            self._chat_completions_url(),
            data=body,
            headers=self._headers(),
            method="POST",
        )

        try:
            with urllib_request.urlopen(request) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib_error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"HTTP {exc.code} from endpoint: {error_body}"
            ) from exc
        except urllib_error.URLError as exc:
            raise RuntimeError(f"Could not reach endpoint: {exc.reason}") from exc

    def run(
        self,
        *,
        prompt_text: str,
        row: dict[str, str],
        max_output_tokens: int,
    ) -> str:
        try:
            response_payload = self._post_json(
                self._payload(
                    prompt_text=prompt_text,
                    row=row,
                    max_output_tokens=max_output_tokens,
                    use_json_mode=True,
                )
            )
        except RuntimeError as exc:
            message = normalize_text(exc).lower()
            if not any(
                marker in message
                for marker in ["response_format", "json_object", "json mode", "unsupported"]
            ):
                raise
            response_payload = self._post_json(
                self._payload(
                    prompt_text=prompt_text,
                    row=row,
                    max_output_tokens=max_output_tokens,
                    use_json_mode=False,
                )
            )

        choices = response_payload.get("choices", [])
        if not choices:
            return json.dumps(response_payload, ensure_ascii=False)

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if isinstance(content, list):
            fragments: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text_value = normalize_text(item.get("text") or item.get("content"))
                else:
                    text_value = normalize_text(item)
                if text_value:
                    fragments.append(text_value)
            return "\n".join(fragments).strip()

        return normalize_text(content)


def run_prompt_evaluation(
    *,
    dataset_rows: list[dict[str, str]],
    prompt_config: PromptConfig,
    model: str,
    max_output_tokens: int,
    force: bool,
    local_runner: LocalHFModelRunner | None,
    endpoint_runner: EndpointModelRunner | None,
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
            if local_runner is not None:
                raw_response = local_runner.run(
                    build_local_generation_prompt(prompt_text, dataset_row),
                    max_new_tokens=max_output_tokens,
                )
            elif endpoint_runner is not None:
                raw_response = endpoint_runner.run(
                    prompt_text=prompt_text,
                    row=dataset_row,
                    max_output_tokens=max_output_tokens,
                )
            else:
                raise RuntimeError("No model runner was configured.")

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

    dataset_path = resolve_project_path(args.dataset_path)
    dataset_rows = load_dataset_rows(dataset_path, max_rows=args.max_rows)
    prompt_configs = build_prompt_configs()

    selected_configs: list[PromptConfig]
    if args.prompt_mode == "both":
        selected_configs = [prompt_configs["direct"], prompt_configs["structured"]]
    else:
        selected_configs = [prompt_configs[args.prompt_mode]]

    base_url = normalize_base_url(args.base_url)
    api_key = normalize_text(args.api_key)
    local_runner: LocalHFModelRunner | None = None
    endpoint_runner: EndpointModelRunner | None = None

    print(f"Dataset: {repo_relative(dataset_path)}")
    print(f"Rows to process: {len(dataset_rows)}")
    print(f"Model: {args.model}")
    if uses_local_transformers_mode(base_url):
        print("Backend: local transformers")
        if args.max_rows != 0:
            local_runner = LocalHFModelRunner(args.model, api_key)
    else:
        print(f"Base URL: {base_url}")
        print("Backend: OpenAI-compatible endpoint")
        endpoint_runner = EndpointModelRunner(args.model, base_url, api_key)
    print(f"Prompt mode: {args.prompt_mode}")

    for prompt_config in selected_configs:
        run_prompt_evaluation(
            dataset_rows=dataset_rows,
            prompt_config=prompt_config,
            model=args.model,
            max_output_tokens=args.max_output_tokens,
            force=args.force,
            local_runner=local_runner,
            endpoint_runner=endpoint_runner,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
