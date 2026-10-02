from __future__ import annotations

import json
from typing import Optional

import httpx

from app.config import settings


def _extract_content(data: dict) -> str:
    try:
        choices = data.get("choices", [])
        if not choices:
            return ""
        message = choices[0].get("message", {})
        content = message.get("content")
        if isinstance(content, list):
            return "".join(part.get("text", "") for part in content if isinstance(part, dict))
        if isinstance(content, str):
            return content
    except Exception:
        pass
    return ""


def generate_text(prompt: str, system_prompt: Optional[str] = None) -> str:
    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        raise RuntimeError("Missing OpenRouter API key in backend/.env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "SmartPrompt",
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "max_tokens": 512,
        "temperature": 0.4,
        "messages": [
            {"role": "system", "content": system_prompt or "You are a helpful workplace communication assistant."},
            {"role": "user", "content": prompt},
        ],
    }

    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=45.0,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"OpenRouter request failed with status {response.status_code}: {response.text[:200]}")

    data = response.json()
    result = _extract_content(data)
    if not result:
        raise RuntimeError("OpenRouter returned an empty response.")
    return result.strip()
