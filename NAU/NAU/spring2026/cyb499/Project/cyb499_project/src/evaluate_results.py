from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSITIVE_LABEL = "Malicious"
NEGATIVE_LABEL = "Benign"
LABEL_ORDER = [NEGATIVE_LABEL, POSITIVE_LABEL]
GROUND_TRUTH_COLUMNS = [
    "ground_truth",
    "label",
    "true_label",
    "expected_label",
]

DIRECT_PREDICTION_COLUMNS = [
    "classification",
    "prediction",
    "predicted_label",
    "predicted_classification",
    "model_prediction",
    "model_classification",
]

JSON_RESPONSE_COLUMNS = [
    "response",
    "model_response",
    "raw_response",
    "assistant_response",
    "output",
    "model_output",
    "completion",
    "raw_output",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate raw model output CSV files against ground-truth labels.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results/raw_model_outputs"),
        help="Directory containing raw model output CSV files.",
    )
    parser.add_argument(
        "--metrics-dir",
        type=Path,
        default=Path("results/metrics"),
        help="Directory where metrics JSON/CSV files will be saved.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("results/figures"),
        help="Directory where confusion matrix figures will be saved.",
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


def normalize_label(value: Any) -> str:
    text = normalize_text(value).lower()
    if text in {"malicious", "mal", "attack", "1", "true"}:
        return POSITIVE_LABEL
    if text in {"benign", "ben", "0", "false"}:
        return NEGATIVE_LABEL
    return ""


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for raw_row in reader:
            row = {
                normalize_text(key): normalize_text(value)
                for key, value in raw_row.items()
                if key is not None
            }
            rows.append(row)
    return rows


def parse_json_response(text: str) -> dict[str, Any]:
    stripped = normalize_text(text)
    if not stripped:
        return {}

    candidates = [stripped]
    first_brace = stripped.find("{")
    last_brace = stripped.rfind("}")
    if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
        candidates.append(stripped[first_brace : last_brace + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    return {}


def extract_prediction(row: dict[str, str]) -> tuple[str, str]:
    for column in DIRECT_PREDICTION_COLUMNS:
        label = normalize_label(row.get(column, ""))
        if label:
            return label, f"direct:{column}"

    for column in JSON_RESPONSE_COLUMNS:
        parsed = parse_json_response(row.get(column, ""))
        label = normalize_label(parsed.get("classification") or parsed.get("prediction"))
        if label:
            return label, f"json:{column}"

    return "", ""


def extract_ground_truth(row: dict[str, str]) -> tuple[str, str]:
    for column in GROUND_TRUTH_COLUMNS:
        label = normalize_label(row.get(column, ""))
        if label:
            return label, column
    return "", ""


def prepare_evaluation_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    prepared: list[dict[str, str]] = []
    for row in rows:
        label, source = extract_prediction(row)
        truth, truth_source = extract_ground_truth(row)
        prepared_row = dict(row)
        prepared_row["predicted_label"] = label
        prepared_row["prediction_source"] = source
        prepared_row["ground_truth_label"] = truth
        prepared_row["ground_truth_source"] = truth_source
        prepared.append(prepared_row)
    return prepared


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def compute_metrics(rows: list[dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    evaluated_rows = [
        row
        for row in rows
        if row.get("ground_truth_label") in LABEL_ORDER and row.get("predicted_label") in LABEL_ORDER
    ]
    if not evaluated_rows:
        raise ValueError("No rows contained both a valid ground truth label and a valid prediction.")

    tn = fp = fn = tp = 0
    for row in evaluated_rows:
        truth = row["ground_truth_label"]
        prediction = row["predicted_label"]

        if truth == NEGATIVE_LABEL and prediction == NEGATIVE_LABEL:
            tn += 1
        elif truth == NEGATIVE_LABEL and prediction == POSITIVE_LABEL:
            fp += 1
        elif truth == POSITIVE_LABEL and prediction == NEGATIVE_LABEL:
            fn += 1
        elif truth == POSITIVE_LABEL and prediction == POSITIVE_LABEL:
            tp += 1

    total = tn + fp + fn + tp
    accuracy = safe_divide(tn + tp, total)
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1_score = safe_divide(2 * precision * recall, precision + recall)

    metrics = {
        "evaluated_rows": total,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "false_positives": fp,
        "false_negatives": fn,
        "confusion_matrix": {
            "labels": LABEL_ORDER,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
            "matrix": [[tn, fp], [fn, tp]],
        },
    }
    return metrics, evaluated_rows


def save_metrics_json(metrics: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def save_summary_csv(summary_rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not summary_rows:
        return

    fieldnames = list(summary_rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)


def svg_fill_color(value: int, max_value: int) -> str:
    if max_value <= 0:
        return "#eef4fb"

    ratio = value / max_value
    red = int(238 - (ratio * 120))
    green = int(244 - (ratio * 90))
    blue = int(251 - (ratio * 20))
    return f"rgb({max(red, 70)},{max(green, 110)},{max(blue, 180)})"


def save_confusion_matrix_figure(
    *,
    matrix: list[list[int]],
    title: str,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    max_value = max(max(row) for row in matrix) if matrix else 0
    cell_size = 110
    x0 = 120
    y0 = 80
    width = 420
    height = 330
    labels = LABEL_ORDER

    cells: list[str] = []
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            x = x0 + (column_index * cell_size)
            y = y0 + (row_index * cell_size)
            fill = svg_fill_color(value, max_value)
            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                f'fill="{fill}" stroke="#2f4f6f" stroke-width="1.5" />'
            )
            cells.append(
                f'<text x="{x + (cell_size / 2)}" y="{y + (cell_size / 2) + 8}" '
                'font-family="Segoe UI, Arial, sans-serif" font-size="28" '
                'text-anchor="middle" fill="#0f2235">'
                f"{value}</text>"
            )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="{width / 2}" y="34" font-family="Segoe UI, Arial, sans-serif" font-size="18" text-anchor="middle" fill="#10263a">{title}</text>
  <text x="{width / 2}" y="58" font-family="Segoe UI, Arial, sans-serif" font-size="12" text-anchor="middle" fill="#4b6278">Predicted Label</text>
  <text x="28" y="{height / 2}" font-family="Segoe UI, Arial, sans-serif" font-size="12" text-anchor="middle" fill="#4b6278" transform="rotate(-90 28 {height / 2})">True Label</text>
  <text x="{x0 + (cell_size / 2)}" y="{y0 - 18}" font-family="Segoe UI, Arial, sans-serif" font-size="13" text-anchor="middle" fill="#18344d">{labels[0]}</text>
  <text x="{x0 + (cell_size * 1.5)}" y="{y0 - 18}" font-family="Segoe UI, Arial, sans-serif" font-size="13" text-anchor="middle" fill="#18344d">{labels[1]}</text>
  <text x="{x0 - 18}" y="{y0 + (cell_size / 2) + 4}" font-family="Segoe UI, Arial, sans-serif" font-size="13" text-anchor="end" fill="#18344d">{labels[0]}</text>
  <text x="{x0 - 18}" y="{y0 + (cell_size * 1.5) + 4}" font-family="Segoe UI, Arial, sans-serif" font-size="13" text-anchor="end" fill="#18344d">{labels[1]}</text>
  {''.join(cells)}
</svg>
"""
    output_path.write_text(svg, encoding="utf-8")


def evaluate_file(
    *,
    predictions_path: Path,
    metrics_dir: Path,
    figures_dir: Path,
) -> dict[str, Any]:
    prediction_rows = load_csv_rows(predictions_path)
    evaluation_rows = prepare_evaluation_rows(prediction_rows)
    metrics, evaluated_rows = compute_metrics(evaluation_rows)

    valid_ground_truth_count = sum(
        1 for row in evaluation_rows if row.get("ground_truth_label") in LABEL_ORDER
    )
    valid_prediction_count = sum(
        1 for row in evaluation_rows if row.get("predicted_label") in LABEL_ORDER
    )
    missing_or_invalid_ground_truth = len(evaluation_rows) - valid_ground_truth_count
    missing_or_invalid_predictions = len(evaluation_rows) - valid_prediction_count

    result_name = predictions_path.stem
    metrics_payload = {
        "input_file": repo_relative(predictions_path),
        "total_rows": len(prediction_rows),
        "valid_ground_truth_rows": valid_ground_truth_count,
        "valid_prediction_rows": valid_prediction_count,
        "missing_or_invalid_ground_truth": missing_or_invalid_ground_truth,
        "missing_or_invalid_predictions": missing_or_invalid_predictions,
        **metrics,
    }

    metrics_path = metrics_dir / f"{result_name}_metrics.json"
    save_metrics_json(metrics_payload, metrics_path)

    figure_path = figures_dir / f"{result_name}_confusion_matrix.svg"
    save_confusion_matrix_figure(
        matrix=metrics["confusion_matrix"]["matrix"],
        title=f"{result_name} Confusion Matrix",
        output_path=figure_path,
    )

    return {
        "input_file": repo_relative(predictions_path),
        "total_rows": len(prediction_rows),
        "valid_ground_truth_rows": valid_ground_truth_count,
        "valid_prediction_rows": valid_prediction_count,
        "evaluated_rows": len(evaluated_rows),
        "missing_or_invalid_ground_truth": missing_or_invalid_ground_truth,
        "missing_or_invalid_predictions": missing_or_invalid_predictions,
        "accuracy": f"{metrics['accuracy']:.6f}",
        "precision": f"{metrics['precision']:.6f}",
        "recall": f"{metrics['recall']:.6f}",
        "f1_score": f"{metrics['f1_score']:.6f}",
        "false_positive": metrics["confusion_matrix"]["false_positive"],
        "false_negative": metrics["confusion_matrix"]["false_negative"],
        "true_negative": metrics["confusion_matrix"]["true_negative"],
        "true_positive": metrics["confusion_matrix"]["true_positive"],
        "metrics_json": repo_relative(metrics_path),
        "confusion_matrix_figure": repo_relative(figure_path),
    }


def main() -> int:
    args = parse_args()
    results_dir = resolve_project_path(args.results_dir)
    metrics_dir = resolve_project_path(args.metrics_dir)
    figures_dir = resolve_project_path(args.figures_dir)

    prediction_files = sorted(results_dir.glob("*.csv"))

    metrics_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Model outputs dir: {repo_relative(results_dir)}")

    if not prediction_files:
        print("No raw model output CSV files were found.")
        return 0

    summary_rows: list[dict[str, Any]] = []
    for predictions_path in prediction_files:
        summary = evaluate_file(
            predictions_path=predictions_path,
            metrics_dir=metrics_dir,
            figures_dir=figures_dir,
        )
        summary_rows.append(summary)

    summary_path = metrics_dir / "evaluation_summary.csv"
    save_summary_csv(summary_rows, summary_path)

    print(f"Saved evaluation summary to {repo_relative(summary_path)}")
    for row in summary_rows:
        print(
            f"{Path(row['input_file']).name}: accuracy={float(row['accuracy']):.4f}, "
            f"precision={float(row['precision']):.4f}, recall={float(row['recall']):.4f}, "
            f"f1={float(row['f1_score']):.4f}, FP={row['false_positive']}, "
            f"FN={row['false_negative']}, evaluated_rows={row['evaluated_rows']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
