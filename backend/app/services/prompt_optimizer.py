from __future__ import annotations

from typing import Dict

PLACEHOLDERS = {
    "manager": "[Manager Name]",
    "date": "[Date]",
    "project": "[Project Name]",
    "reason": "[Reason]",
    "days": "[Number of Days]",
    "recipient": "[Recipient Name]",
    "deadline": "[Deadline]",
    "context": "[Additional Context]",
}


def optimize_prompt(prompt: str, prompt_type: str) -> str:
    lower = prompt.lower()

    if "email" in lower or "message" in lower:
        body = (
            "Act as a professional workplace communication assistant.\n\n"
            "Write a concise and professional email to [Manager Name] or [Recipient Name] regarding [Purpose/Topic].\n\n"
            "Context:\n"
            "- Background: [Additional Context]\n"
            "- Relevant details: [Project/Issue/Reason]\n"
            "- Date: [Date]\n"
            "- Deadline or follow-up: [Deadline]\n\n"
            "Requirements:\n"
            "- Use a professional and respectful tone.\n"
            "- Clearly state the purpose of the email.\n"
            "- Include all key facts and dates.\n"
            "- Keep the message concise and easy to read.\n"
            "- End with a professional closing.\n\n"
            "Return only the email."
        )
        return body

    if "leave" in lower or "vacation" in lower or "pto" in lower:
        return (
            "Act as a professional workplace assistant.\n\n"
            "Draft a formal leave request email to [Manager Name].\n\n"
            "Include the following details:\n"
            "- Leave dates: [Start Date] to [End Date]\n"
            "- Reason: [Reason]\n"
            "- Number of days: [Number of Days]\n"
            "- Work coverage or handover plan: [Handover Details]\n"
            "- Department or team: [Department/Team]\n\n"
            "Requirements:\n"
            "- Use a respectful and professional tone.\n"
            "- Keep the request clear and brief.\n"
            "- Mention the purpose and dates clearly.\n"
            "- End with a polite closing.\n\n"
            "Return only the leave request."
        )

    if "project" in lower and ("report" in lower or "update" in lower or "summary" in lower):
        return (
            "Act as a professional workplace analyst.\n\n"
            "Write a clear project update or project report for [Manager Name].\n\n"
            "Context:\n"
            "- Project: [Project Name]\n"
            "- Current status: [Status]\n"
            "- Completed work: [Completed Work]\n"
            "- Pending work: [Pending Work]\n"
            "- Blockers: [Blockers]\n"
            "- Deadline: [Deadline]\n\n"
            "Requirements:\n"
            "- Use a professional and concise tone.\n"
            "- Summarize progress, risks, and next steps clearly.\n"
            "- Include a short status overview and action items.\n"
            "- Keep the output structured and easy to scan.\n\n"
            "Return only the project update."
        )

    if "meeting" in lower and ("summary" in lower or "minutes" in lower):
        return (
            "Act as a professional meeting coordinator.\n\n"
            "Summarize the meeting for [Team/Department].\n\n"
            "Context:\n"
            "- Meeting topic: [Topic]\n"
            "- Date: [Date]\n"
            "- Attendees: [Names/Teams]\n"
            "- Key decisions: [Decisions]\n"
            "- Action items: [Action Items]\n\n"
            "Requirements:\n"
            "- Use a concise business tone.\n"
            "- Include decisions, next steps, and owners.\n"
            "- Keep the summary structured with headings if helpful.\n\n"
            "Return only the meeting summary."
        )

    if "hr" in lower or "human resources" in lower:
        return (
            "Act as a professional HR communication assistant.\n\n"
            "Write a respectful HR communication regarding [Topic].\n\n"
            "Context:\n"
            "- Employee or sender: [Name/Role]\n"
            "- Recipient: [HR Team/Manager]\n"
            "- Relevant issue or request: [Issue/Request]\n"
            "- Supporting details: [Date/Department/Policy context]\n\n"
            "Requirements:\n"
            "- Use a respectful and professional tone.\n"
            "- State the purpose clearly.\n"
            "- Include all required facts and context.\n"
            "- Keep the message concise and formal.\n\n"
            "Return only the HR communication."
        )

    if "resume" in lower or "cv" in lower or "cover letter" in lower:
        return (
            "Act as a professional career advisor.\n\n"
            "Write a polished professional resume or career document for [Candidate Name].\n\n"
            "Context:\n"
            "- Role target: [Job Title/Industry]\n"
            "- Education: [Education Details]\n"
            "- Experience: [Experience Summary]\n"
            "- Skills: [Skills]\n"
            "- Achievements: [Achievements]\n\n"
            "Requirements:\n"
            "- Use a professional and clear tone.\n"
            "- Highlight relevant qualifications and experience.\n"
            "- Keep the output easy to scan and well-structured.\n\n"
            "Return only the resume content."
        )

    return (
        "Act as an expert workplace prompt engineer.\n\n"
        f"Improve the following workplace request while preserving its original intent:\n\n{prompt}\n\n"
        "Requirements:\n"
        "- Add missing audience and context where needed.\n"
        "- Use placeholders for unknown user-specific details such as [Manager Name], [Date], [Project Name], or [Reason].\n"
        "- Make the task clear, specific, and professional.\n"
        "- Add a useful output format when helpful.\n"
        "- Preserve the user's original intent without inventing personal facts.\n\n"
        "Return only the improved prompt."
    )
