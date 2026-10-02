from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.schemas import AnalyzeRequest, CompareRequest, GenerateRequest
from app.services.constraint_detector import detect_constraints
from app.services.gap_analyzer import analyze_gap
from app.services.output_evaluator import evaluate_outputs
from app.services.prompt_identifier import identify_prompt
from app.services.prompt_optimizer import optimize_prompt
from app.services.prompt_scorer import calculate_score
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = exc.errors()
    if any(item.get("loc", ("",))[-1] == "prompt" for item in details):
        return JSONResponse(status_code=400, content={"detail": "Prompt cannot be empty."})
    return JSONResponse(status_code=422, content={"detail": details})


@app.get("/health")
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze(payload: AnalyzeRequest) -> Dict[str, Any]:
    text = (payload.prompt or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    prompt_type_data = identify_prompt(text)
    detected_constraints = detect_constraints(text)
    gap_analysis = analyze_gap(text)
    original_score, breakdown = calculate_score(text, gap_analysis)
    optimized = optimize_prompt(text, prompt_type_data["prompt_type"])
    optimized_score, optimized_breakdown = calculate_score(optimized, analyze_gap(optimized))

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
        "detected_constraints": detected_constraints,
        "gap_analysis": gap_analysis,
        "optimized_prompt": optimized,
        "optimized_score": optimized_score,
        "optimized_breakdown": optimized_breakdown,
        "summary": summary,
        "metadata": {
            "dataset_summary": {
                "total_records": DATASET_STATS.get("total_records", 0),
                "available_constraint_categories": DATASET_STATS.get("constraint_categories", []),
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
        return {"output": output}
    except Exception as exc:
        return {"error": "Unable to generate the response right now. Please check your API configuration or try again.", "details": str(exc)[:200]}


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
    except Exception:
        return {
            "error": "Unable to generate the response right now. Please check your API configuration or try again.",
            "original_prompt": text,
            "optimized_prompt": optimized_prompt,
            "original_output": "",
            "optimized_output": "",
            "evaluation": {"summary": "No output generated due to OpenRouter availability."},
        }

    evaluation = evaluate_outputs(original_output, optimized_output, text)
    return {
        "original_prompt": text,
        "optimized_prompt": optimized_prompt,
        "original_output": original_output,
        "optimized_output": optimized_output,
        "analysis": analysis,
        "evaluation": evaluation,
    }


@app.get("/api/examples")
async def examples() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "label": "Write an email to my manager.", "prompt": "Write an email to my manager."},
        {"id": 2, "label": "Write a leave request.", "prompt": "Write a leave request."},
        {"id": 3, "label": "Make a report about my project.", "prompt": "Make a report about my project."},
        {"id": 4, "label": "Summarize this meeting.", "prompt": "Summarize this meeting."},
        {"id": 5, "label": "Write a message to HR.", "prompt": "Write a message to HR."},
        {"id": 6, "label": "Write a project update for my manager.", "prompt": "Write a project update for my manager."},
        {"id": 7, "label": "Create a task description for a software developer.", "prompt": "Create a task description for a software developer."},
        {"id": 8, "label": "Write a professional email to a client.", "prompt": "Write a professional email to a client."},
        {"id": 9, "label": "Write a performance review.", "prompt": "Write a performance review."},
        {"id": 10, "label": "Create a presentation outline for my project.", "prompt": "Create a presentation outline for my project."},
    ]


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
            "instruction_types": DATASET_STATS.get("instruction_types", {}),
            "constraint_categories": DATASET_STATS.get("constraint_categories", []),
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
