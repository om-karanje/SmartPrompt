from __future__ import annotations

import re
from typing import Dict, List


def analyze_gap(prompt: str) -> List[Dict[str, str]]:
    text = prompt.strip()
    lower = text.lower()

    def status_for(condition: bool, partial_condition: bool = False) -> str:
        if condition:
            return "present"
        if partial_condition:
            return "partial"
        return "missing"

    role = status_for(bool(re.search(r"\b(act as|you are|as a|assistant|professional)\b", lower)))
    task = status_for(bool(re.search(r"\b(write|draft|create|summarize|generate|prepare|make|review|analyze|describe)\b", lower)))
    context = status_for(
        bool(re.search(r"\b(about|regarding|for|project|meeting|client|manager|team|hr|department|deadline|date|reason)\b", lower)),
        bool(re.search(r"\b(context|background|details)\b", lower)),
    )
    objective = status_for(bool(re.search(r"\b(goal|aim|purpose|objective|to\s+[a-z]|so that|want to)\b", lower)), bool("to" in lower))
    audience = status_for(bool(re.search(r"\b(manager|boss|team|client|friend|hr|audience|recipient|coworker)\b", lower)))
    tone = status_for(bool(re.search(r"\b(professional|formal|friendly|casual|concise|respectful|angry|warm|kind|neutral)\b", lower)))
    output_format = status_for(
        bool(re.search(r"\b(email|report|summary|json|markdown|bullet|table|paragraph|poem|essay|title|outline)\b", lower)),
        bool(re.search(r"\b(format|structure|style)\b", lower)),
    )
    length = status_for(bool(re.search(r"\b(\d+\s+words?|\d+\s+sentences?|\d+\s+paragraphs?|\d+\s+bullet points?)\b", lower)))
    constraints = status_for(bool(re.search(r"\b(must|should|do not|don't|avoid|without|at least|exactly|less than|more than|only|no\s+[a-z]+)\b", lower)))
    required_information = status_for(
        bool(re.search(r"\b(include|mention|provide|list|state|detail|specific|key facts|deadline|dates?|reason|project name|manager name)\b", lower)),
        bool(re.search(r"\b([a-z]+\s+name|date|reason|details)\b", lower)),
    )
    examples = status_for(bool(re.search(r"\b(for example|such as|example|like)\b", lower)))

    explanations = {
        "Role": "The prompt states or implies the role of the assistant or audience." if role == "present" else "The role of the AI is not clearly specified.",
        "Task": "The requested action is explicit and identifiable." if task == "present" else "The task is vague or not clearly defined.",
        "Context": "Relevant background or project details are included in the request." if context == "present" else "No clear context is provided for the scenario.",
        "Objective": "The prompt shows a clear purpose or intended outcome." if objective == "present" else "The desired outcome is not explicitly defined.",
        "Audience": "The intended reader or recipient is identified." if audience == "present" else "No audience or recipient is specified.",
        "Tone": "The requested tone or style is specified." if tone == "present" else "No tone requirement is provided.",
        "Output Format": "The output format is clearly specified." if output_format == "present" else "The response format is not fully specified.",
        "Length": "A length or size requirement is included." if length == "present" else "No length requirement is specified.",
        "Constraints": "The prompt includes clear constraints or rules." if constraints == "present" else "No explicit constraints are included.",
        "Required Information": "Key facts or required details are present." if required_information == "present" else "Important facts or required details are missing.",
        "Examples": "The prompt gives a helpful example or pattern to follow." if examples == "present" else "No example or reference format is included.",
    }

    components = [
        {"component": "Role", "status": role, "explanation": explanations["Role"]},
        {"component": "Task", "status": task, "explanation": explanations["Task"]},
        {"component": "Context", "status": context, "explanation": explanations["Context"]},
        {"component": "Objective", "status": objective, "explanation": explanations["Objective"]},
        {"component": "Audience", "status": audience, "explanation": explanations["Audience"]},
        {"component": "Tone", "status": tone, "explanation": explanations["Tone"]},
        {"component": "Output Format", "status": output_format, "explanation": explanations["Output Format"]},
        {"component": "Length", "status": length, "explanation": explanations["Length"]},
        {"component": "Constraints", "status": constraints, "explanation": explanations["Constraints"]},
        {"component": "Required Information", "status": required_information, "explanation": explanations["Required Information"]},
        {"component": "Examples", "status": examples, "explanation": explanations["Examples"]},
    ]
    return components
