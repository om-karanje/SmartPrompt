from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.services.constraint_detector import detect_constraints
from app.services.dataset_retriever import find_similar_examples
from app.services.gap_analyzer import analyze_gap
from app.services.llm_service import generate_text
from app.services.output_evaluator import evaluate_outputs
from app.services.prompt_identifier import identify_prompt
from app.services.prompt_optimizer import optimize_prompt
from app.services.prompt_scorer import COMPONENT_WEIGHTS, calculate_score
from app.utils.dataset_loader import load_dataset


def test_identifier_for_email_prompt():
    result = identify_prompt("Write an email to my manager.")
    assert result["prompt_type"] == "Workplace Email"
    assert result["domain"] == "Employee / Workplace"


def test_scoring_has_valid_range_and_breakdown():
    gap = analyze_gap("Write an email to my manager.")
    score, breakdown = calculate_score(gap)
    assert 0 <= score <= 100
    assert sum(breakdown.values()) == score
    assert len(breakdown) == 11
    assert set(breakdown) == set(COMPONENT_WEIGHTS)
    assert sum(COMPONENT_WEIGHTS.values()) == 100


def test_constraint_detector_reports_requested_counts_and_terms():
    constraints = detect_constraints(
        "Write an email with exactly 5 bullet points. Include the keywords 'owner' and 'date'. "
        "Do not use the words 'late' or 'delay'."
    )

    by_type = {item["type"]: item for item in constraints}
    assert by_type["bullet_count"]["status"] == "present"
    assert "5" in by_type["bullet_count"]["detail"]
    assert "owner, date" in by_type["required_terms"]["detail"]
    assert "late, delay" in by_type["forbidden_terms"]["detail"]


def test_gap_analysis_detects_missing_components():
    gap = analyze_gap("Write an email to my manager.")
    missing = [item for item in gap if item["status"] == "missing"]
    assert missing
    present = [item for item in gap if item["status"] == "present"]
    assert present


def test_optimizer_keeps_intent_and_uses_placeholders():
    original = "Write an email to my manager."
    optimized = optimize_prompt(original, "Workplace Email")
    assert "email" in optimized.lower()
    assert original in optimized
    assert "[Intended Audience]" in optimized
    assert "professional" in optimized.lower()


def test_dataset_loader_statistics_are_calculated():
    stats = load_dataset()
    assert stats["total_records"] > 0
    assert isinstance(stats["constraint_types"], dict)
    assert stats["categories"]


def test_examples_endpoint_serves_curated_dataset():
    response = TestClient(app).get("/api/examples")
    assert response.status_code == 200
    examples = response.json()
    assert len(examples) == 500
    assert all({"id", "label", "prompt", "category", "constraints"} <= example.keys() for example in examples)


def test_dataset_retrieval_finds_exact_example_and_optimizer_uses_it():
    examples = load_dataset()["examples"]
    sample = next(example for example in examples if example["id"] == "wp-027")
    matches = find_similar_examples(sample["prompt"], examples)

    assert matches
    assert matches[0]["id"] == sample["id"]
    optimized = optimize_prompt(
        sample["prompt"],
        "Project Update",
        dataset_matches=matches,
    )
    assert "Dataset guidance:" in optimized
    assert sample["label"] in optimized


def test_analyze_endpoint_returns_all_component_scores_and_dataset_matches():
    response = TestClient(app).post(
        "/api/analyze",
        json={"prompt": "Write an update about a project migration with completed work and blockers."},
    )

    assert response.status_code == 200
    result = response.json()
    assert len(result["gap_analysis"]) == 11
    assert len(result["score_breakdown"]) == 11
    assert result["score"] == sum(result["score_breakdown"].values())
    assert result["prompt_type"] == "Project Communication"
    assert result["dataset_matches"]
    assert result["optimized_prompt"].startswith("Act as a professional workplace assistant.")
    assert result["optimized_score"] > result["score"]
    assert next(item for item in result["optimized_gap_analysis"] if item["component"] == "Length")["status"] == "partial"


def test_compare_endpoint_compares_both_generated_outputs():
    with patch("app.main.generate_text", side_effect=["Original response.", "Optimized response."]):
        response = TestClient(app).post(
            "/api/compare",
            json={"prompt": "Write an update about the project."},
        )

    assert response.status_code == 200
    result = response.json()
    assert result["original_output"] == "Original response."
    assert result["optimized_output"] == "Optimized response."
    assert result["evaluation"]["scores"]


def test_compare_endpoint_surfaces_generation_failure():
    with patch("app.main.generate_text", side_effect=RuntimeError("missing API key")):
        response = TestClient(app).post(
            "/api/compare",
            json={"prompt": "Write an update about the project."},
        )

    assert response.status_code == 502
    assert "missing API key" in response.json()["detail"]


def test_output_comparison_uses_prompt_terms_and_labels_heuristic_scores():
    evaluation = evaluate_outputs(
        "The quarterly budget forecast summarizes costs and variance.",
        "The office schedule covers the holiday closure.",
        "Summarize the quarterly budget forecast and variance.",
    )

    scores = evaluation["scores"]
    assert scores["Relevance"]["Original"] > scores["Relevance"]["Optimized"]
    assert "heuristic" in evaluation["summary"].lower()


def test_generate_text_cap_request_size_for_openrouter():
    response = httpx.Response(
        200,
        json={
            "choices": [{
                "message": {
                    "content": "Subject: Team Update\n\nHello team,"
                }
            }]
        },
    )

    with patch("app.services.llm_service.settings.OPENROUTER_API_KEY", "test-key"), \
         patch("app.services.llm_service.settings.OPENROUTER_MODEL", "openai/gpt-4o-mini"), \
         patch("app.services.llm_service.httpx.post", return_value=response) as mock_post:
        result = generate_text("Write an email to my manager.")

    assert result.startswith("Subject:")
    payload = mock_post.call_args.kwargs["json"]
    assert payload["max_tokens"] <= 1024
    assert payload["temperature"] <= 0.9


def test_empty_prompt_returns_clear_validation_error():
    client = TestClient(app)
    response = client.post("/api/analyze", json={"prompt": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Prompt cannot be empty."
