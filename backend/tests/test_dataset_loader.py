import json

import pytest

from app.utils.dataset_loader import load_dataset


def test_dataset_loader_loads_system_ready_workplace_records():
    stats = load_dataset()
    assert stats["total_records"] == 500
    assert len(stats["examples"]) == 500
    assert "projects" in stats["categories"]
    assert stats["constraint_types"]["format"] > 0


def test_dataset_loader_rejects_malformed_records(tmp_path):
    dataset_path = tmp_path / "invalid.jsonl"
    dataset_path.write_text(json.dumps({"id": "missing-fields"}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing or invalid 'label'"):
        load_dataset(dataset_path)


def test_dataset_loader_rejects_duplicate_ids(tmp_path):
    example = {
        "id": "duplicate",
        "label": "Example",
        "prompt": "Write a project update.",
        "category": "projects",
        "constraints": [],
        "source": "original",
        "source_id": None,
    }
    dataset_path = tmp_path / "duplicate.jsonl"
    dataset_path.write_text(
        "\n".join(json.dumps(example) for _ in range(2)),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate dataset id"):
        load_dataset(dataset_path)


def test_dataset_loader_rejects_duplicate_prompts(tmp_path):
    examples = [
        {
            "id": f"example-{index}",
            "label": "Project update",
            "prompt": prompt,
            "category": "projects",
            "constraints": [],
            "source": "original",
            "source_id": None,
        }
        for index, prompt in enumerate(
            ["Write a project update.", "  WRITE A PROJECT UPDATE.  "]
        )
    ]
    dataset_path = tmp_path / "duplicate-prompts.jsonl"
    dataset_path.write_text(
        "\n".join(json.dumps(example) for example in examples),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate dataset prompt"):
        load_dataset(dataset_path)
