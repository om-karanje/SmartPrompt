from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT_DIR / "data" / "ifeval_input_data.jsonl"


def load_dataset(dataset_path: str | Path | None = None) -> Dict[str, Any]:
    resolved_path = Path(dataset_path) if dataset_path else DATASET_PATH
    if not resolved_path.is_absolute():
        if resolved_path.exists():
            file_path = resolved_path
        else:
            project_root = ROOT_DIR.parent
            alternate = project_root / resolved_path
            file_path = alternate if alternate.exists() else resolved_path
    else:
        file_path = resolved_path

    stats: Dict[str, Any] = {
        "file_path": str(file_path),
        "total_records": 0,
        "malformed_records": 0,
        "instruction_types": {},
        "constraint_categories": [],
        "sample_prompts": [],
    }

    if not file_path.exists():
        return stats

    instruction_counter: Counter[str] = Counter()
    category_counter: Counter[str] = Counter()

    with file_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                stats["malformed_records"] += 1
                continue

            if not isinstance(record, dict):
                stats["malformed_records"] += 1
                continue

            stats["total_records"] += 1
            prompt = record.get("prompt", "")
            if prompt and len(stats["sample_prompts"]) < 5:
                stats["sample_prompts"].append(prompt)

            instruction_ids = record.get("instruction_id_list", [])
            if isinstance(instruction_ids, list):
                for instruction_id in instruction_ids:
                    if isinstance(instruction_id, str):
                        instruction_counter[instruction_id] += 1
                        category = instruction_id.split(":", 1)[0]
                        category_counter[category] += 1

    stats["instruction_types"] = dict(sorted(instruction_counter.items(), key=lambda item: (-item[1], item[0])))
    stats["constraint_categories"] = sorted(category_counter)
    return stats
