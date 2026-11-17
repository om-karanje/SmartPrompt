from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT_DIR / "data" / "workplace_prompt_dataset.jsonl"


def _resolve_path(dataset_path: str | Path | None) -> Path:
    if dataset_path is None:
        return DATASET_PATH

    path = Path(dataset_path)
    if path.is_absolute() or path.exists():
        return path

    project_root = ROOT_DIR.parent
    alternate = project_root / path
    return alternate if alternate.exists() else path


def _validate_record(record: Any, line_number: int) -> Dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError(f"Dataset line {line_number} must contain a JSON object.")

    for field in ("id", "label", "prompt", "category", "source"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Dataset line {line_number} has a missing or invalid '{field}'.")

    if record["source"] not in {"ifeval", "original"}:
        raise ValueError(f"Dataset line {line_number} has an unsupported source.")

    constraints = record.get("constraints")
    if not isinstance(constraints, list):
        raise ValueError(f"Dataset line {line_number} must have a constraints list.")

    for constraint in constraints:
        if (
            not isinstance(constraint, dict)
            or not isinstance(constraint.get("type"), str)
            or not constraint["type"].strip()
            or "value" not in constraint
        ):
            raise ValueError(
                f"Dataset line {line_number} contains a constraint without a type and value."
            )

    if record["source"] == "ifeval" and not isinstance(record.get("source_id"), int):
        raise ValueError(f"Dataset line {line_number} must have an integer IFEval source_id.")
    if record["source"] == "original" and record.get("source_id") is not None:
        raise ValueError(f"Dataset line {line_number} must not have a source_id for original data.")

    return record


def load_dataset(dataset_path: str | Path | None = None) -> Dict[str, Any]:
    file_path = _resolve_path(dataset_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Workplace prompt dataset not found: {file_path}")

    examples: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_prompts: set[str] = set()
    category_counter: Counter[str] = Counter()
    constraint_counter: Counter[str] = Counter()

    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                raw_record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on dataset line {line_number}: {exc.msg}") from exc

            record = _validate_record(raw_record, line_number)
            if record["id"] in seen_ids:
                raise ValueError(f"Duplicate dataset id '{record['id']}' on line {line_number}.")
            normalized_prompt = " ".join(record["prompt"].split()).casefold()
            if normalized_prompt in seen_prompts:
                raise ValueError(f"Duplicate dataset prompt on line {line_number}.")

            seen_ids.add(record["id"])
            seen_prompts.add(normalized_prompt)
            examples.append(record)
            category_counter[record["category"]] += 1
            for constraint in record["constraints"]:
                constraint_counter[constraint["type"]] += 1

    if not examples:
        raise ValueError(f"Workplace prompt dataset is empty: {file_path}")

    return {
        "file_path": str(file_path),
        "total_records": len(examples),
        "categories": sorted(category_counter),
        "category_counts": dict(sorted(category_counter.items())),
        "constraint_types": dict(sorted(constraint_counter.items())),
        "examples": examples,
    }
