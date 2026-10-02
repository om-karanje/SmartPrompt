from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.services.gap_analyzer import analyze_gap
from app.services.llm_service import generate_text
from app.services.prompt_identifier import identify_prompt
from app.services.prompt_optimizer import optimize_prompt
from app.services.prompt_scorer import calculate_score
from app.utils.dataset_loader import load_dataset


def test_identifier_for_email_prompt():
    result = identify_prompt("Write an email to my manager.")
    assert result["prompt_type"] == "Workplace Email"
    assert result["domain"] == "Employee / Workplace"


def test_scoring_has_valid_range_and_breakdown():
    gap = analyze_gap("Write an email to my manager.")
    score, breakdown = calculate_score("Write an email to my manager.", gap)
    assert 0 <= score <= 100
    assert sum(breakdown.values()) == score or abs(sum(breakdown.values()) - score) <= 5


def test_gap_analysis_detects_missing_components():
    gap = analyze_gap("Write an email to my manager.")
    missing = [item for item in gap if item["status"] == "missing"]
    assert missing
    present = [item for item in gap if item["status"] == "present"]
    assert present


def test_optimizer_keeps_intent_and_uses_placeholders():
    optimized = optimize_prompt("Write an email to my manager.", "Workplace Email")
    assert "email" in optimized.lower()
    assert "[Manager Name]" in optimized or "[Recipient Name]" in optimized
    assert "professional" in optimized.lower()


def test_dataset_loader_statistics_are_calculated():
    stats = load_dataset()
    assert stats["total_records"] > 0
    assert isinstance(stats["instruction_types"], dict)
    assert stats["constraint_categories"]


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
