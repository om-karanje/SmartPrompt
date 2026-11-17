from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import HTTPError

from app.schemas import AnalysisResponse, AnalyzeRequest, CompareRequest, DatasetExample, GenerateRequest
from app.services.constraint_detector import detect_constraints
from app.services.dataset_retriever import find_similar_examples
from app.services.gap_analyzer import analyze_gap
from app.services.output_evaluator import evaluate_outputs
from app.services.prompt_identifier import identify_prompt
from app.services.prompt_optimizer import optimize_prompt
from app.services.prompt_scorer import COMPONENT_WEIGHTS, calculate_score
from app.services.llm_service import generate_text
from app.utils.dataset_loader import load_dataset

app = FastAPI(title="SmartPrompt API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATASET_STATS = load_dataset()
DATASET_EXAMPLES = DATASET_STATS["examples"]
DATASET_CATEGORY_CLASSIFICATION = {
    "client_communication": ("Client Communication", "Client-facing communication"),
    "customer_support": ("Customer Support", "Customer issue resolution"),
    "human_resources": ("HR Communication", "HR and policy communication"),
    "internal_communications": ("Internal Communication", "Workplace announcements"),
    "learning_and_development": ("Learning and Development", "Workplace learning"),
    "leave_and_time_off": ("Leave Request", "Leave and time-off management"),
    "meetings": ("Meeting Support", "Meeting coordination and documentation"),
    "onboarding": ("Onboarding", "New employee onboarding"),
    "operations": ("Operations", "Workplace operations"),
    "performance_management": ("Performance Review", "Performance evaluation"),
    "projects": ("Project Communication", "Project planning and progress reporting"),
    "recruitment": ("Recruitment", "Hiring and candidate evaluation"),
    "task_management": ("Task Planning", "Task definition and assignment"),
    "team_management": ("Team Management", "Team coordination"),
    "vendor_management": ("Vendor Communication", "Vendor coordination"),
}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = exc.errors()
    if any(item.get("loc", ("",))[-1] == "prompt" for item in details):
        return JSONResponse(status_code=400, content={"detail": "Prompt cannot be empty."})
    return JSONResponse(status_code=422, content={"detail": details})


@app.get("/health")
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(payload: AnalyzeRequest) -> Dict[str, Any]:
    text = (payload.prompt or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    prompt_type_data = identify_prompt(text)
    dataset_matches = find_similar_examples(text, DATASET_EXAMPLES)
    if (
        prompt_type_data["prompt_type"] == "General Workplace Request"
        and dataset_matches
        and dataset_matches[0]["similarity"] >= 0.2
    ):
        classification = DATASET_CATEGORY_CLASSIFICATION.get(dataset_matches[0]["category"])
        if classification:
            prompt_type_data["prompt_type"], prompt_type_data["intent"] = classification

    detected_constraints = detect_constraints(text)
    gap_analysis = analyze_gap(text)
    original_score, breakdown = calculate_score(gap_analysis)
    optimized = optimize_prompt(
        text,
        prompt_type_data["prompt_type"],
        gap_analysis=gap_analysis,
        detected_constraints=detected_constraints,
        dataset_matches=dataset_matches,
    )
    optimized_gap_analysis = analyze_gap(optimized)
    optimized_score, optimized_breakdown = calculate_score(optimized_gap_analysis)

    summary = (
        f"Detected as a {prompt_type_data['prompt_type']} prompt. "
        f"The prompt is {prompt_type_data['intent'].lower()} and is missing "
        f"{sum(1 for item in gap_analysis if item['status'] == 'missing')} key workplace details."
    )

    return {
        "prompt_type": prompt_type_data["prompt_type"],
        "domain": prompt_type_data["domain"],
        "intent": prompt_type_data["intent"],
        "score": original_score,
        "score_breakdown": breakdown,
        "score_weights": COMPONENT_WEIGHTS,
        "detected_constraints": detected_constraints,
        "gap_analysis": gap_analysis,
        "optimized_prompt": optimized,
        "optimized_score": optimized_score,
        "optimized_score_breakdown": optimized_breakdown,
        "optimized_score_weights": COMPONENT_WEIGHTS,
        "optimized_gap_analysis": optimized_gap_analysis,
        "dataset_matches": dataset_matches,
        "summary": summary,
        "metadata": {
            "dataset_summary": {
                "total_records": DATASET_STATS.get("total_records", 0),
                "workplace_categories": DATASET_STATS.get("categories", []),
            }
        }
    }


@app.post("/api/generate")
async def generate(payload: GenerateRequest) -> Dict[str, Any]:
    text = (payload.prompt or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        output = generate_text(text)
    except (HTTPError, RuntimeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to generate a response: {exc}",
        ) from exc
    return {"output": output}


@app.post("/api/compare")
async def compare(payload: CompareRequest) -> Dict[str, Any]:
    text = (payload.prompt or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    analysis = await analyze(AnalyzeRequest(prompt=text))
    optimized_prompt = analysis["optimized_prompt"]

    try:
        original_output = generate_text(text)
        optimized_output = generate_text(optimized_prompt)
    except (HTTPError, RuntimeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to compare outputs: {exc}",
        ) from exc

    evaluation = evaluate_outputs(original_output, optimized_output, text)
    return {
        "original_prompt": text,
        "optimized_prompt": optimized_prompt,
        "original_output": original_output,
        "optimized_output": optimized_output,
        "analysis": analysis,
        "evaluation": evaluation,
    }


@app.get("/api/examples", response_model=List[DatasetExample])
async def examples() -> List[Dict[str, Any]]:
    return DATASET_EXAMPLES


@app.get("/api/statistics")
async def statistics() -> Dict[str, Any]:
    return {
        "total_prompts_analyzed": 0,
        "average_original_score": 0,
        "average_optimized_score": 0,
        "average_improvement": 0,
        "most_common_prompt_type": "No analysis data available yet.",
        "most_common_missing_component": "No analysis data available yet.",
        "total_detected_constraints": 0,
        "dataset": {
            "total_records": DATASET_STATS.get("total_records", 0),
            "categories": DATASET_STATS.get("categories", []),
            "category_counts": DATASET_STATS.get("category_counts", {}),
            "constraint_types": DATASET_STATS.get("constraint_types", {}),
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
