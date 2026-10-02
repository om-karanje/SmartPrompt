from __future__ import annotations

import re
from typing import Dict


def identify_prompt(prompt: str) -> Dict[str, str]:
    text = prompt.lower()

    patterns = {
        "Workplace Email": [
            "email", "manager", "boss", "colleague", "client", "coworker", "professional email",
            "send an email", "write an email"
        ],
        "Leave Request": [
            "leave request", "vacation", "pto", "sick leave", "personal leave", "annual leave", "time off"
        ],
        "HR Communication": ["hr", "human resources", "policy", "benefits", "payroll", "attendance", "employee"],
        "Project Update": ["project update", "status update", "progress update", "update on my project"],
        "Project Report": ["project report", "project summary", "status report", "report about my project"],
        "Meeting Summary": ["meeting summary", "summarize this meeting", "minutes", "agenda"],
        "Task Description": ["task description", "job description", "responsibilities", "software developer", "developer task"],
        "Performance Review": ["performance review", "evaluation", "peer feedback", "review for", "annual review"],
        "Client Communication": ["client", "customer", "vendor", "stakeholder", "proposal", "meeting with client"],
        "Professional Message": ["message to", "professional message", "professional note", "workplace message"],
        "Presentation / Report Generation": ["presentation", "slide deck", "report generation", "outline for my project"],
        "Resume / Career Prompt": ["resume", "cv", "cover letter", "career", "job application"],
        "General Workplace Request": ["workplace", "team", "manager", "office", "work", "organization"],
    }

    match_type = "General Workplace Request"
    matched_intent = "Professional communication"

    for prompt_type, keywords in patterns.items():
        if any(keyword in text for keyword in keywords):
            match_type = prompt_type
            break

    if match_type == "Workplace Email":
        matched_intent = "Professional communication"
    elif match_type == "Leave Request":
        matched_intent = "Leave and time-off management"
    elif match_type == "HR Communication":
        matched_intent = "HR and policy communication"
    elif match_type == "Project Update":
        matched_intent = "Progress reporting"
    elif match_type == "Project Report":
        matched_intent = "Status reporting and documentation"
    elif match_type == "Meeting Summary":
        matched_intent = "Meeting documentation"
    elif match_type == "Task Description":
        matched_intent = "Task planning and assignment"
    elif match_type == "Performance Review":
        matched_intent = "Performance evaluation"
    elif match_type == "Client Communication":
        matched_intent = "Client-facing communication"
    elif match_type == "Professional Message":
        matched_intent = "Workplace messaging"
    elif match_type == "Presentation / Report Generation":
        matched_intent = "Structured presentation and report drafting"
    elif match_type == "Resume / Career Prompt":
        matched_intent = "Career and professional development"
    else:
        matched_intent = "General workplace request"

    if re.search(r"\b(leave|vacation|pto|sick)\b", text):
        match_type = "Leave Request"
    if re.search(r"\b(hr|human resources|benefits|policy|payroll)\b", text):
        match_type = "HR Communication"
    if re.search(r"\b(meeting|agenda|minut|summary)\b", text):
        match_type = "Meeting Summary"
    if re.search(r"\b(resume|cv|cover letter|career)\b", text):
        match_type = "Resume / Career Prompt"

    return {
        "prompt_type": match_type,
        "domain": "Employee / Workplace",
        "intent": matched_intent,
    }
