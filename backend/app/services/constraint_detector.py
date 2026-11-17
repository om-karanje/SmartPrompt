from __future__ import annotations

import re
from typing import Any, Dict, List


def detect_constraints(prompt: str) -> List[Dict[str, Any]]:
    detected: List[Dict[str, Any]] = []

    def add(constraint_type: str, label: str, detail: str) -> None:
        if not any(item["type"] == constraint_type for item in detected):
            detected.append({
                "type": constraint_type,
                "label": label,
                "detail": detail,
                "status": "present",
            })

    count_patterns = [
        (
            "word_count",
            "Word count requirement",
            r"\b(no more than|maximum(?: of)?|max(?:imum)?|up to|at least|minimum(?: of)?|more than|exactly|less than|at most|fewer than)\s+(\d+)\s+words?\b",
        ),
        (
            "sentence_count",
            "Sentence count requirement",
            r"\b(no more than|maximum(?: of)?|max(?:imum)?|up to|at least|minimum(?: of)?|more than|exactly|less than|at most|fewer than)\s+(\d+)\s+sentences?\b",
        ),
        (
            "bullet_count",
            "Bullet count requirement",
            r"\b(no more than|maximum(?: of)?|max(?:imum)?|up to|at least|minimum(?: of)?|more than|exactly|less than|at most|fewer than)\s+(\d+)\s+(?:bullet points?|bullets?)\b",
        ),
        (
            "paragraph_count",
            "Paragraph count requirement",
            r"\b(no more than|maximum(?: of)?|max(?:imum)?|up to|at least|minimum(?: of)?|more than|exactly|less than|at most|fewer than)\s+(\d+)\s+paragraphs?\b",
        ),
    ]
    for constraint_type, label, pattern in count_patterns:
        match = re.search(pattern, prompt, re.I)
        if match:
            add(
                constraint_type,
                label,
                f"Requires {match.group(1).lower()} {match.group(2)} {constraint_type.replace('_count', 's')}.",
            )

    lower_text = prompt.casefold()
    if re.search(r"\b(?:bullet|bullets|bullet list)\b", lower_text):
        add("bullet_list", "Bullet list required", "Prompt asks for a bullet-list format.")

    required_clause = re.search(
        r"\b(?:include|contain|mention|use)\b[^.!?\n]*",
        prompt,
        re.I,
    )
    if required_clause and re.search(r"\b(?:keywords?|terms?|words?)\b", required_clause.group(0), re.I):
        quoted_terms = re.findall(r"[\"']([^\"']+)[\"']", required_clause.group(0))
        detail = (
            f"Required terms: {', '.join(quoted_terms)}."
            if quoted_terms
            else "Prompt requires one or more keywords or terms."
        )
        add("required_terms", "Keyword requirement", detail)

    forbidden_clause = re.search(
        r"\b(?:do not use|don't use|avoid|forbidden|must not include|do not include)\b"
        r"[^.!?\n]*",
        prompt,
        re.I,
    )
    if forbidden_clause and re.search(r"\b(?:words?|keywords?|terms?)\b", forbidden_clause.group(0), re.I):
        quoted_terms = re.findall(r"[\"']([^\"']+)[\"']", forbidden_clause.group(0))
        detail = (
            f"Forbidden terms: {', '.join(quoted_terms)}."
            if quoted_terms
            else "Prompt specifies words or terms to avoid."
        )
        add("forbidden_terms", "Forbidden content", detail)

    if re.search(r"\b(?:all lowercase|lowercase|all lower case|lower case)\b", lower_text):
        add("letter_case", "Case requirement", "Prompt requires lowercase output.")
    if re.search(r"\b(?:all uppercase|uppercase|all upper case|upper case|capital letters)\b", lower_text):
        add("letter_case", "Case requirement", "Prompt requires uppercase output.")
    if re.search(r"\b(?:in english|english only|use only.*language|respond in.*language)\b", lower_text):
        add("language", "Language requirement", "Prompt specifies a response language.")
    if re.search(r"\b(?:in json|json format|markdown|bullet list|as a table|in a table)\b", lower_text):
        add("format", "Formatting requirement", "Prompt specifies an output format.")
    if re.search(r"\b(?:title|header|section|paragraph|divider)\b", lower_text):
        add("structure", "Structural requirement", "Prompt requires a title or sectioned structure.")

    if not detected:
        detected.append({
            "type": "none",
            "label": "No explicit constraints detected",
            "detail": "No clear instruction-following constraint was found in the prompt.",
            "status": "warning",
        })

    return detected
