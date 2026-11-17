from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence


FORMAT_LABELS = {
    "approval_request": "approval request",
    "campaign_brief": "campaign brief",
    "checklist": "checklist",
    "closeout_report": "project closeout report",
    "decision_log_entry": "decision log entry",
    "decision_request": "decision request",
    "email": "email",
    "handoff": "handoff note",
    "meeting_summary": "meeting summary",
    "message": "workplace message",
    "performance_review": "performance review",
    "requirements_summary": "requirements summary",
    "scorecard": "scorecard",
    "status_update": "status update",
    "summary": "summary",
    "task_brief": "task brief",
    "triage_report": "triage report",
}


def _example_hint(dataset_matches: Sequence[Dict[str, Any]]) -> str:
    if not dataset_matches or dataset_matches[0].get("similarity", 0) < 0.12:
        return ""

    match = dataset_matches[0]
    formats: List[str] = []
    sections: List[str] = []
    for constraint in match.get("constraints", []):
        constraint_type = constraint.get("type")
        value = constraint.get("value")
        if constraint_type in {"required_fields", "required_sections", "required_topics"}:
            if isinstance(value, list):
                sections.extend(str(item) for item in value)
        elif constraint_type == "format" and isinstance(value, str):
            formats.append(FORMAT_LABELS.get(value, value.replace("_", " ")))

    guidance: List[str] = []
    if formats:
        guidance.append(f"the {formats[0]} format")
    if sections:
        guidance.append(f"sections such as {', '.join(list(dict.fromkeys(sections))[:5])}")
    if not guidance:
        return (
            f"Optional reference: a similar workplace example is "
            f"'{match['label']}' in the {match['category'].replace('_', ' ')} category. "
            "Use its structure only when it fits the original request."
        )

    return (
        f"Optional reference from the similar dataset example '{match['label']}': "
        f"consider {' and '.join(guidance)} only when they fit the original request."
    )


def optimize_prompt(
    prompt: str,
    prompt_type: str,
    *,
    gap_analysis: Optional[List[Dict[str, str]]] = None,
    detected_constraints: Optional[List[Dict[str, Any]]] = None,
    dataset_matches: Optional[Sequence[Dict[str, Any]]] = None,
) -> str:
    statuses = {
        item["component"]: item["status"]
        for item in gap_analysis or []
    }
    constraints = detected_constraints or []
    matches = dataset_matches or []
    example_hint = _example_hint(matches)
    best_match = matches[0] if matches and matches[0].get("similarity", 0) >= 0.12 else None

    tone = "the tone specified in the request"
    if statuses.get("Tone") in {None, "missing"}:
        tone = "a professional and respectful tone"
        if best_match:
            matched_tones = [
                constraint.get("value")
                for constraint in best_match.get("constraints", [])
                if constraint.get("type") == "tone"
                and isinstance(constraint.get("value"), str)
            ]
            if matched_tones:
                tone = f"a {matched_tones[0].replace('_', ' ')} tone"

    output_format = "the output format specified in the request"
    if statuses.get("Output Format") in {None, "missing"}:
        output_format = f"a clear format suitable for a {prompt_type.lower()}"

    constraint_lines = [
        f"- {item['label']}: {item['detail']}"
        for item in constraints
        if item.get("status") == "present"
        and item.get("label") != "No explicit constraints detected"
    ]
    if not constraint_lines:
        constraint_lines = [
            "- Preserve every explicit instruction in the original request.",
            "- Do not invent personal, project, date, or business facts.",
        ]

    sections = [
        "Act as a professional workplace assistant.",
        f"Request type: {prompt_type}.",
        "Task and original request (preserve its intent and explicit requirements):",
        prompt.strip(),
        "Objective: Complete the original request clearly and accurately.",
        "Context: Use facts from the original request; mark missing context as [Additional Context] instead of guessing.",
        "Audience: Address [Intended Audience] unless the original request specifies one.",
        f"Tone: Use {tone}.",
        f"Output format: Use {output_format}.",
        "Length: Follow the requested length, or use [Target Length] if none was specified.",
        "Constraints:",
        *constraint_lines,
        "Required information: Include relevant facts and supplied names, dates, decisions, or next steps; use placeholders for missing details.",
        "Example: Follow any reference example in the original request; otherwise use [Reference Example] only if one is needed.",
    ]
    if example_hint:
        sections.extend(["Dataset guidance:", example_hint])
    sections.append("Return only the requested workplace content.")
    return "\n\n".join(sections)
