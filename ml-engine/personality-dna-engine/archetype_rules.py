from typing import Dict, Any

def evaluate_archetype_rules(features: Dict[str, Any]) -> Dict[str, float]:
    """
    Evaluates rule-based heuristic conditions on engineered indicators
    to return a membership score (0 to 100) for each of the 5 financial archetypes.
    """
    savings = features.get("savings_behavior_score", 50.0)
    discipline = features.get("discipline_score", 50.0)
    goal_commitment = features.get("goal_commitment_score", 50.0)
    impulse_risk = features.get("impulse_risk_score", 50.0)
    stability = features.get("financial_stability_score", 50.0)
    exploration = features.get("exploration_score", 50.0)
    budget_consistency = features.get("budget_consistency_score", 50.0)
    stress_resilience = features.get("stress_resilience_score", 50.0)

    # 1. Planner Score (High discipline, high budget adherence, strong goal completion, low stress)
    planner_score = (discipline + budget_consistency + goal_commitment + stress_resilience) / 4.0

    # 2. Saver Score (High savings behavior, low discretionary exploration, high discipline)
    saver_score = (savings + (100.0 - exploration) + discipline) / 3.0

    # 3. Impulse Buyer Score (High impulse score, low discipline, low budget consistency)
    impulse_buyer_score = (impulse_risk + (100.0 - discipline) + (100.0 - budget_consistency)) / 3.0

    # 4. Explorer Score (High experience spending, moderate savings, low-to-moderate discipline)
    explorer_score = (exploration + savings + (100.0 - discipline)) / 3.0

    # 5. Dreamer Score (Inconsistent saving/discipline, low goal completion despite goals)
    dreamer_score = ((100.0 - goal_commitment) + (100.0 - discipline) + savings) / 3.0

    return {
        "Planner": float(max(0.0, min(100.0, planner_score))),
        "Saver": float(max(0.0, min(100.0, saver_score))),
        "Impulse Buyer": float(max(0.0, min(100.0, impulse_buyer_score))),
        "Explorer": float(max(0.0, min(100.0, explorer_score))),
        "Dreamer": float(max(0.0, min(100.0, dreamer_score)))
    }
