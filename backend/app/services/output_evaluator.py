from __future__ import annotations

import re
from typing import Any, Dict


def _score_field(text: str) -> int:
    words = re.findall(r"\b\w+\b", text)
    return max(1, min(100, len(words) // 2))


def evaluate_outputs(original_output: str, optimized_output: str, original_prompt: str) -> Dict[str, Any]:
    original_words = len(re.findall(r"\b\w+\b", original_output or ""))
    optimized_words = len(re.findall(r"\b\w+\b", optimized_output or ""))

    def evaluate(text: str, label: str) -> Dict[str, int]:
        word_count = len(re.findall(r"\b\w+\b", text or ""))
        structure_bonus = 15 if any(marker in text for marker in ["- ", "1.", "2.", "***", "Dear", "Subject", "Summary"]) else 0
        specificity_bonus = 15 if word_count > 60 else 5
        relevance_bonus = 15 if any(term in text.lower() for term in ["project", "manager", "team", "deadline", "report", "email", "summary"]) else 5
        tone_bonus = 15 if any(term in text.lower() for term in ["professional", "respectfully", "please", "regards", "sincerely", "concise"]) else 5
        return {
            "Relevance": max(30, min(100, 45 + relevance_bonus + (10 if word_count > 40 else 0))),
            "Completeness": max(30, min(100, 40 + specificity_bonus + structure_bonus)),
            "Structure": max(35, min(100, 35 + structure_bonus + (5 if word_count > 30 else 0))),
            "Specificity": max(30, min(100, 40 + specificity_bonus + (10 if any(ch.isdigit() for ch in text) else 0))),
            "Instruction Adherence": max(35, min(100, 50 + (10 if word_count > 25 else 0) + structure_bonus // 2)),
            "Professional Tone": max(30, min(100, 40 + tone_bonus + (10 if word_count > 30 else 0))),
        }

    original_scores = evaluate(original_output, "Original")
    optimized_scores = evaluate(optimized_output, "Optimized")

    summary = (
        "The optimized output is typically clearer, more structured, and more specific because it follows the improved prompt and adds relevant workplace context."
        if optimized_words >= original_words
        else "The optimized output is comparable in length but may benefit from more explicit context or structure."
    )

    return {
        "scores": {
            "Relevance": {"Original": original_scores["Relevance"], "Optimized": optimized_scores["Relevance"]},
            "Completeness": {"Original": original_scores["Completeness"], "Optimized": optimized_scores["Completeness"]},
            "Structure": {"Original": original_scores["Structure"], "Optimized": optimized_scores["Structure"]},
            "Specificity": {"Original": original_scores["Specificity"], "Optimized": optimized_scores["Specificity"]},
            "Instruction Adherence": {"Original": original_scores["Instruction Adherence"], "Optimized": optimized_scores["Instruction Adherence"]},
            "Professional Tone": {"Original": original_scores["Professional Tone"], "Optimized": optimized_scores["Professional Tone"]},
        },
        "summary": summary,
        "original_word_count": original_words,
        "optimized_word_count": optimized_words,
    }
