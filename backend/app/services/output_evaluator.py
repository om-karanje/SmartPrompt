from __future__ import annotations

import re
from typing import Any, Dict


def evaluate_outputs(original_output: str, optimized_output: str, original_prompt: str) -> Dict[str, Any]:
    original_words = len(re.findall(r"\b\w+\b", original_output or ""))
    optimized_words = len(re.findall(r"\b\w+\b", optimized_output or ""))
    prompt_terms = set(re.findall(r"\b[a-z0-9]{3,}\b", original_prompt.casefold()))
    prompt_terms.difference_update({"about", "after", "before", "from", "into", "that", "then", "this", "with", "write"})

    def evaluate(text: str) -> Dict[str, int]:
        word_count = len(re.findall(r"\b\w+\b", text or ""))
        output_terms = set(re.findall(r"\b[a-z0-9]{3,}\b", text.casefold()))
        structure_bonus = 15 if any(marker in text for marker in ["- ", "1.", "2.", "***", "Dear", "Subject", "Summary"]) else 0
        specificity_bonus = 15 if word_count > 60 else 5
        tone_bonus = 15 if any(term in text.lower() for term in ["professional", "respectfully", "please", "regards", "sincerely", "concise"]) else 5
        relevance = (
            50
            if not prompt_terms
            else 35 + round(65 * len(prompt_terms & output_terms) / len(prompt_terms))
        )
        return {
            "Relevance": max(30, min(100, relevance)),
            "Completeness": max(30, min(100, 40 + specificity_bonus + structure_bonus)),
            "Structure": max(35, min(100, 35 + structure_bonus + (5 if word_count > 30 else 0))),
            "Specificity": max(30, min(100, 40 + specificity_bonus + (10 if any(ch.isdigit() for ch in text) else 0))),
            "Instruction Adherence": max(35, min(100, 50 + (10 if word_count > 25 else 0) + structure_bonus // 2)),
            "Professional Tone": max(30, min(100, 40 + tone_bonus + (10 if word_count > 30 else 0))),
        }

    original_scores = evaluate(original_output)
    optimized_scores = evaluate(optimized_output)
    improved_dimensions = sum(
        optimized_scores[key] > original_scores[key]
        for key in original_scores
    )
    declined_dimensions = sum(
        optimized_scores[key] < original_scores[key]
        for key in original_scores
    )

    if improved_dimensions > declined_dimensions:
        summary = (
            f"The optimized output scored higher in {improved_dimensions} of "
            f"{len(original_scores)} heuristic dimensions. Review it for factual accuracy "
            "and instruction compliance before use."
        )
    elif declined_dimensions > improved_dimensions:
        summary = (
            f"The original output scored higher in {declined_dimensions} of "
            f"{len(original_scores)} heuristic dimensions. Review both responses against "
            "the original request."
        )
    else:
        summary = (
            "The outputs received similar heuristic scores. Review both responses for "
            "factual accuracy and instruction compliance."
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
