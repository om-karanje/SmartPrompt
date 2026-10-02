from __future__ import annotations

from typing import Dict, List, Tuple

from app.utils.scoring_utils import score_from_status


DIMENSIONS = [
    ("Clarity", 20, ["Role", "Task", "Objective"]),
    ("Specificity", 20, ["Required Information", "Context", "Task"]),
    ("Context", 15, ["Context", "Required Information"]),
    ("Task Definition", 15, ["Task", "Objective"]),
    ("Output Format", 10, ["Output Format", "Length"]),
    ("Constraints", 10, ["Constraints", "Length"]),
    ("Audience & Tone", 10, ["Audience", "Tone"]),
]


def calculate_score(prompt: str, gap_analysis: List[Dict[str, str]]) -> Tuple[int, Dict[str, int]]:
    status_by_component = {item["component"]: item["status"] for item in gap_analysis}

    score_breakdown = {}
    for label, weight, components in DIMENSIONS:
        statuses = {component: status_by_component.get(component, "missing") for component in components}
        score_breakdown[label] = score_from_status(statuses, weight)

    if len(prompt.strip()) > 80:
        score_breakdown["Clarity"] = min(score_breakdown["Clarity"] + 2, 20)
    if len(prompt.strip()) > 200:
        score_breakdown["Specificity"] = min(score_breakdown["Specificity"] + 2, 20)

    total = sum(score_breakdown.values())
    return total, score_breakdown
