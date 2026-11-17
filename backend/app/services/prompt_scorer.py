from __future__ import annotations

from typing import Dict, List, Tuple

from app.utils.scoring_utils import score_from_status


COMPONENT_WEIGHTS = {
    "Role": 8,
    "Task": 12,
    "Context": 10,
    "Objective": 8,
    "Audience": 10,
    "Tone": 7,
    "Output Format": 10,
    "Length": 7,
    "Constraints": 10,
    "Required Information": 10,
    "Examples": 8,
}


def calculate_score(gap_analysis: List[Dict[str, str]]) -> Tuple[int, Dict[str, int]]:
    status_by_component = {item["component"]: item["status"] for item in gap_analysis}

    score_breakdown = {
        component: score_from_status(
            {component: status_by_component.get(component, "missing")},
            weight,
        )
        for component, weight in COMPONENT_WEIGHTS.items()
    }
    return sum(score_breakdown.values()), score_breakdown
