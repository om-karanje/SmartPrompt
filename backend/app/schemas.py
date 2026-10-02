from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Workplace prompt to analyze")


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Prompt to send to the LLM")


class CompareRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Original workplace prompt")


class ExampleItem(BaseModel):
    id: int
    label: str
    prompt: str


class AnalysisResponse(BaseModel):
    prompt_type: str
    domain: str
    intent: str
    score: int
    score_breakdown: Dict[str, int]
    detected_constraints: List[Dict[str, Any]]
    gap_analysis: List[Dict[str, Any]]
    optimized_prompt: str
    optimized_score: int
    summary: str
    metadata: Optional[Dict[str, Any]] = None
