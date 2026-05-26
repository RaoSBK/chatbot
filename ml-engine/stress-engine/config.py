# Configuration file for Financial Stress Score Engine

# Factor Weights
WEIGHT_BUDGET = 0.25
WEIGHT_SAVINGS = 0.20
WEIGHT_GOAL_PROGRESS = 0.15
WEIGHT_IMPULSE_SPENDING = 0.15
WEIGHT_VOLATILITY = 0.10
WEIGHT_WEEKEND_OVERSPENDING = 0.05
WEIGHT_SUBSCRIPTIONS = 0.05
WEIGHT_CATEGORY_SPIKES = 0.05

# Stress Level Classification Brackets
CLASS_BRACKETS = [
    {"min": 80, "max": 100, "label": "Financially Healthy"},
    {"min": 60, "max": 79, "label": "Stable"},
    {"min": 40, "max": 59, "label": "Needs Attention"},
    {"min": 20, "max": 39, "label": "High Financial Stress"},
    {"min": 0, "max": 19, "label": "Critical"}
]

def classify_stress_level(score: float) -> str:
    """Classifies a stress score into a text-based stress level."""
    rounded_score = int(round(score))
    # Bound score
    rounded_score = max(0, min(100, rounded_score))
    
    for bracket in CLASS_BRACKETS:
        if bracket["min"] <= rounded_score <= bracket["max"]:
            return bracket["label"]
            
    return "Stable" # Default fallback
