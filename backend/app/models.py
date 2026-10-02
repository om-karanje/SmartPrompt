from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PromptAnalysisResult:
    prompt_type: str
    domain: str
    intent: str
    score: int
    score_breakdown: Dict[str, int]
    detected_constraints: List[Dict[str, Any]]
    gap_analysis: List[Dict[str, Any]]
    optimized_prompt: str
    optimized_score: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    original_prompt: str
    optimized_prompt: str
    original_output: str
    optimized_output: str
    evaluation: Dict[str, Any]
