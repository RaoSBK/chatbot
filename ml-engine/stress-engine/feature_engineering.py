from typing import Dict, Any

def engineer_features(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms raw user metrics and pattern engine outputs into engineered financial stress indicators.
    """
    income = float(raw_data.get("monthly_income", 30000.0))
    savings = float(raw_data.get("savings", 0.0))
    budget_utilization = float(raw_data.get("budget_utilization", 0.0))
    goal_progress = float(raw_data.get("goal_progress", 0.0))
    spending_volatility = float(raw_data.get("spending_volatility", 0.0))
    impulse_score = float(raw_data.get("impulse_score", 0.0))
    weekend_ratio = float(raw_data.get("weekend_ratio", 1.0))
    subscription_count = int(raw_data.get("subscription_count", 0))
    category_spikes = int(raw_data.get("category_spikes", 0))

    # 1. Savings Rate (ratio of savings to income)
    savings_rate = float(savings / income) if income > 0.0 else 0.0

    # 2. Budget Pressure (normalized utilization ratio)
    budget_pressure = float(budget_utilization / 100.0)

    # 3. Volatility Index
    volatility_index = float(spending_volatility)

    # 4. Goal Health Score (ratio of goal completion)
    goal_health_score = float(goal_progress / 100.0)

    # 5. Impulse Risk
    impulse_risk = float(impulse_score)

    # 6. Weekend Risk
    weekend_risk = float(weekend_ratio)

    # 7. Subscription Burden
    subscription_burden = float(subscription_count)

    # 8. Category Risk
    category_risk = float(category_spikes)

    return {
        "savings_rate": savings_rate,
        "budget_pressure": budget_pressure,
        "volatility_index": volatility_index,
        "goal_health_score": goal_health_score,
        "impulse_risk": impulse_risk,
        "weekend_risk": weekend_risk,
        "subscription_burden": subscription_burden,
        "category_risk": category_risk
    }
