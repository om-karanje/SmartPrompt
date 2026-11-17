from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Dict, Iterable, List, Set


STOP_WORDS = {
    "a", "about", "after", "all", "an", "and", "any", "are", "as", "at", "be",
    "before", "by", "can", "create", "do", "for", "from", "help", "how", "i",
    "in", "include", "is", "it", "me", "my", "of", "on", "or", "our", "please",
    "provide", "should", "some", "the", "their", "them", "there", "this", "to",
    "we", "what", "when", "where", "which", "who", "with", "write", "you",
}


def _tokens(value: str) -> Set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) > 1 and token not in STOP_WORDS
    }


def _constraint_text(constraints: Iterable[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for constraint in constraints:
        parts.append(str(constraint.get("type", "")))
        value = constraint.get("value")
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif isinstance(value, (str, int, float)):
            parts.append(str(value))
    return " ".join(parts)


def find_similar_examples(
    prompt: str,
    examples: List[Dict[str, Any]],
    limit: int = 3,
) -> List[Dict[str, Any]]:
    query_tokens = _tokens(prompt)
    if not query_tokens or not examples or limit < 1:
        return []

    documents: List[tuple[Dict[str, Any], Set[str], Set[str]]] = []
    document_frequency: Counter[str] = Counter()
    for example in examples:
        label_tokens = _tokens(example.get("label", ""))
        category_tokens = _tokens(example.get("category", ""))
        document_tokens = (
            _tokens(example.get("prompt", ""))
            | label_tokens
            | category_tokens
            | _tokens(_constraint_text(example.get("constraints", [])))
        )
        documents.append((example, document_tokens, label_tokens | category_tokens))
        document_frequency.update(document_tokens)

    inverse_document_frequency = {
        token: math.log(
            1 + (len(documents) - document_frequency[token] + 0.5)
            / (document_frequency[token] + 0.5)
        )
        for token in query_tokens
    }
    total_query_weight = sum(inverse_document_frequency.values())
    if not total_query_weight:
        return []

    matches: List[Dict[str, Any]] = []
    for example, document_tokens, boosted_tokens in documents:
        matched_tokens = query_tokens & document_tokens
        if not matched_tokens:
            continue
        weight = sum(
            inverse_document_frequency[token] * (1.5 if token in boosted_tokens else 1)
            for token in matched_tokens
        )
        similarity = min(1.0, weight / total_query_weight)
        match = dict(example)
        match["similarity"] = round(similarity, 3)
        matches.append(match)

    matches.sort(key=lambda item: (-item["similarity"], item["id"]))
    return matches[:limit]
