from app.utils.dataset_loader import load_dataset


def test_dataset_loader_loads_valid_jsonl():
    stats = load_dataset('backend/data/ifeval_input_data.jsonl')
    assert stats['total_records'] > 0
    assert 'instruction_types' in stats
    assert 'constraint_categories' in stats


def test_dataset_loader_handles_malformed_entries():
    stats = load_dataset('backend/data/ifeval_input_data.jsonl')
    assert stats['malformed_records'] >= 0
