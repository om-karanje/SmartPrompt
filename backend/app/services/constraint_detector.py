from __future__ import annotations

import re
from typing import Any, Dict, List


def detect_constraints(prompt: str) -> List[Dict[str, Any]]:
    text = prompt.strip()
    lower_text = text.lower()
    detected: List[Dict[str, Any]] = []

    checks = []

    if re.search(r"\b(?:bullet|bullets|bullet list)\b", lower_text, re.I):
        checks.append(("Bullet list required", "Prompt asks for a bullet list."))
    if re.search(r"\b(?:at least|minimum|more than|exactly|less than|at most|fewer than)\s+\d+\s+words?\b", lower_text, re.I):
        checks.append(("Word count requirement", "Prompt specifies a word requirement."))
    if re.search(r"\b(?:at least|minimum|more than|exactly|less than|at most|fewer than)\s+\d+\s+sentences?\b", lower_text, re.I):
        checks.append(("Sentence count requirement", "Prompt specifies a sentence constraint."))
    if re.search(r"\b(?:must include|include|contains|mention)\s+[\"\']?[a-zA-Z0-9 _-]+[\"\']?\b", lower_text, re.I):
        checks.append(("Keyword requirement", "Prompt includes a keyword or required term requirement."))
    if re.search(r"\b(?:do not|don't|avoid|forbidden|not include|without)\s+[\"\']?[a-zA-Z0-9 _-]+[\"\']?\b", lower_text, re.I):
        checks.append(("Forbidden content", "Prompt indicates wording to avoid."))
    if re.search(r"\b(?:all lowercase|lowercase|all lower case|lower case)\b", lower_text, re.I):
        checks.append(("Case requirement", "Prompt requires lowercase output."))
    if re.search(r"\b(?:all uppercase|uppercase|all upper case|upper case|capital letters)\b", lower_text, re.I):
        checks.append(("Case requirement", "Prompt requires uppercase output."))
    if re.search(r"\b(?:json|markdown|email|bullet list|table|poem|essay)\b", lower_text, re.I):
        checks.append(("Formatting requirement", "Prompt specifies an output format."))
    if re.search(r"\b(?:in english|english only|use only.*language|respond in.*language)\b", lower_text, re.I):
        checks.append(("Language requirement", "Prompt specifies a language constraint."))
    if re.search(r"\b(?:title|header|section|paragraph|divider)\b", lower_text, re.I):
        checks.append(("Structural requirement", "Prompt requires a title or sectioned structure."))

    for label, detail in checks:
        detected.append({"label": label, "detail": detail, "status": "present"})

    if not detected:
        detected.append({"label": "No explicit constraints detected", "detail": "No clear instruction-following constraint was found in the prompt.", "status": "warning"})

    return detected
