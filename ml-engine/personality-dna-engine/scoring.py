# Scoring helper utilities for Financial Personality DNA Engine

from typing import List, Dict, Any

def normalize_score(value: float, min_val: float, max_val: float) -> float:
    """
    Scales and caps a raw value to a [0.0, 100.0] score range.
    """
    if max_val <= min_val:
        return 0.0
    scaled = (value - min_val) / (max_val - min_val) * 100.0
    return float(max(0.0, min(100.0, scaled)))

def compute_average_indicator(scores: List[float]) -> float:
    """
    Computes standard mean average across a list of financial indices.
    """
    if not scores:
        return 0.0
    return float(sum(scores) / len(scores))
