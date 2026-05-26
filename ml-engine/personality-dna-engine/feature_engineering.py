from typing import Dict, Any

def engineer_features(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms raw user financial profiles, stress outputs, and category distributions
    into engineered behavioral personality metrics.
    """
    savings_rate = float(raw_data.get("savings_rate", 0.0))
    stress_score = float(raw_data.get("stress_score", 50.0))
    weekend_ratio = float(raw_data.get("weekend_ratio", 1.0))
    impulse_score = float(raw_data.get("impulse_score", 0.0))
    goal_completion_rate = float(raw_data.get("goal_completion_rate", 0.0))
    budget_adherence = float(raw_data.get("budget_adherence", 0.0))
    spending_volatility = float(raw_data.get("spending_volatility", 0.0))
    category_distribution = raw_data.get("category_distribution", {})

    # 1. Savings Behavior Score (scaled up to 100 at 25% savings rate)
    savings_behavior_score = float(min(100.0, (savings_rate / 0.25) * 100.0)) if savings_rate > 0.0 else 0.0

    # 2. Discipline Score (combines budget adherence and low impulse)
    discipline_score = float((budget_adherence * 0.6 + (1.0 - impulse_score) * 0.4) * 100.0)

    # 3. Goal Commitment Score
    goal_commitment_score = float(goal_completion_rate * 100.0)

    # 4. Impulse Risk Score
    impulse_risk_score = float(impulse_score * 100.0)

    # 5. Financial Stability Score
    financial_stability_score = float(stress_score)

    # 6. Exploration Score (experiences spending: travel, shopping, entertainment, leisure)
    # Sum up discretionary category percentage ratios
    # Supports both integer percentage inputs (e.g. 20) and float ratios (e.g. 0.20)
    discretionary_categories = ["travel", "shopping", "entertainment", "leisure", "dining", "food"]
    discretionary_total = 0.0
    for cat, val in category_distribution.items():
        if cat.lower() in discretionary_categories:
            amount = float(val)
            # Standardize: if value is < 1.0 (e.g. 0.20), scale it to percent (20)
            if amount < 1.0:
                amount *= 100.0
            discretionary_total += amount
            
    exploration_score = float(min(100.0, discretionary_total))

    # 7. Budget Consistency Score
    budget_consistency_score = float(budget_adherence * 100.0)

    # 8. Stress Resilience Score
    stress_resilience_score = float(stress_score)

    return {
        "savings_behavior_score": savings_behavior_score,
        "discipline_score": discipline_score,
        "goal_commitment_score": goal_commitment_score,
        "impulse_risk_score": impulse_risk_score,
        "financial_stability_score": financial_stability_score,
        "exploration_score": exploration_score,
        "budget_consistency_score": budget_consistency_score,
        "stress_resilience_score": stress_resilience_score
    }
