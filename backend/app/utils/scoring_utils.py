from typing import Dict, Union


STATUS_WEIGHTS = {
    "present": 1.0,
    "partial": 0.5,
    "missing": 0.0,
}


def status_value(status: str) -> float:
    return STATUS_WEIGHTS.get(status, 0.0)


def clamp_score(value: Union[int, float], minimum: int = 0, maximum: int = 100) -> int:
    numeric = float(value)
    return max(minimum, min(maximum, int(round(numeric))))


def score_from_status(statuses: Dict[str, str], weight: int) -> int:
    if not statuses:
        return 0
    average = sum(status_value(item) for item in statuses.values()) / len(statuses)
    return clamp_score(weight * average)
