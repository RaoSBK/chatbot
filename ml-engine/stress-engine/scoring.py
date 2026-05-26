from typing import Dict, Any

from config import (
    WEIGHT_BUDGET,
    WEIGHT_SAVINGS,
    WEIGHT_GOAL_PROGRESS,
    WEIGHT_IMPULSE_SPENDING,
    WEIGHT_VOLATILITY,
    WEIGHT_WEEKEND_OVERSPENDING,
    WEIGHT_SUBSCRIPTIONS,
    WEIGHT_CATEGORY_SPIKES
)

def calculate_weighted_score(features: Dict[str, Any]) -> float:
    """
    Translates individual engineered financial features into sub-scores from 0 to 100,
    and aggregates them into a final weighted stress-free score (0-100).
    A score of 100 represents extremely healthy; 0 represents critical stress.
    """
    # 1. Budget Sub-score (100 is healthy, 0 is fully utilized/over-budget)
    budget_utilization = features.get("budget_pressure", 0.0) * 100.0
    if budget_utilization <= 40.0:
        budget_score = 100.0
    elif budget_utilization >= 100.0:
        budget_score = 0.0
    else:
        budget_score = max(0.0, min(100.0, 100.0 - (budget_utilization - 40.0) / 60.0 * 100.0))

    # 2. Savings Sub-score (100 is highly saving [>=30%], 0 is no savings)
    savings_rate = features.get("savings_rate", 0.0)
    if savings_rate >= 0.30:
        savings_score = 100.0
    elif savings_rate <= 0.0:
        savings_score = 0.0
    else:
        savings_score = max(0.0, min(100.0, (savings_rate / 0.30) * 100.0))

    # 3. Goal Progress Sub-score (100 is complete, 0 is no progress)
    goal_score = features.get("goal_health_score", 0.0) * 100.0
    goal_score = max(0.0, min(100.0, goal_score))

    # 4. Impulse Spending Sub-score (100 is low impulse risk, 0 is extremely impulsive)
    impulse_risk = features.get("impulse_risk", 0.0)
    impulse_score_sub = max(0.0, min(100.0, (1.0 - impulse_risk) * 100.0))

    # 5. Volatility Sub-score (100 is stable daily spend, 0 is highly erratic)
    volatility_index = features.get("volatility_index", 0.0)
    volatility_score = max(0.0, min(100.0, (1.0 - volatility_index) * 100.0))

    # 6. Weekend Overspending Sub-score (100 is low weekend ratio [<=0.2], 0 is high [>=1.5])
    weekend_risk = features.get("weekend_risk", 1.0)
    if weekend_risk <= 0.20:
        weekend_score = 100.0
    elif weekend_risk >= 1.50:
        weekend_score = 0.0
    else:
        weekend_score = max(0.0, min(100.0, (1.50 - weekend_risk) / 1.30 * 100.0))

    # 7. Subscription Burden Sub-score (100 is low [<=2], 0 is high [>=8])
    subscription_burden = features.get("subscription_burden", 0.0)
    if subscription_burden <= 2.0:
        sub_score = 100.0
    elif subscription_burden >= 8.0:
        sub_score = 0.0
    else:
        sub_score = max(0.0, min(100.0, (8.0 - subscription_burden) / 6.0 * 100.0))

    # 8. Category Risk Sub-score (100 is no spikes, 0 is high [>=5])
    category_risk = features.get("category_risk", 0.0)
    if category_risk == 0.0:
        category_score = 100.0
    elif category_risk >= 5.0:
        category_score = 0.0
    else:
        category_score = max(0.0, min(100.0, (5.0 - category_risk) / 5.0 * 100.0))

    # Weighted Aggregation
    final_score = (
        WEIGHT_BUDGET * budget_score +
        WEIGHT_SAVINGS * savings_score +
        WEIGHT_GOAL_PROGRESS * goal_score +
        WEIGHT_IMPULSE_SPENDING * impulse_score_sub +
        WEIGHT_VOLATILITY * volatility_score +
        WEIGHT_WEEKEND_OVERSPENDING * weekend_score +
        WEIGHT_SUBSCRIPTIONS * sub_score +
        WEIGHT_CATEGORY_SPIKES * category_score
    )

    return float(max(0.0, min(100.0, final_score)))
