from typing import List, Dict, Any

def generate_insights(patterns: List[Dict[str, Any]], classification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes rule-based patterns and ML classification profiles into structured, actionable insights
    to be consumed by downstream coaching scoring engines.
    """
    # Expose downstream flags
    discretionary_spikes = [p for p in patterns if p["pattern_type"] == "Category Spending Spike"]
    weekend_overspend = [p for p in patterns if p["pattern_type"] == "Weekend Overspending"]
    anomalies = [p for p in patterns if p["pattern_type"] == "Unusual Expense Detection"]
    subscriptions = [p for p in patterns if p["pattern_type"] == "Subscription Detection"]

    # downstream consumer hooks
    financial_stress_indicators = {
        "has_high_volatility": any(p["severity"] == "High" for p in patterns),
        "weekend_drain": len(weekend_overspend) > 0 and weekend_overspend[0]["severity"] == "High",
        "salary_spike_detected": any(p["pattern_type"] == "Salary-Day Spending Spike" for p in patterns),
        "unusual_spike_count": len(anomalies)
    }

    financial_personality_markers = {
        "predominant_spending_profile": classification.get("profile_class", "Balanced Spender"),
        "impulse_index": classification.get("impulse_score", 0.0),
        "saving_readiness": "Low" if classification.get("profile_class") == "Impulse Spender" else "High" if classification.get("profile_class") == "Disciplined Saver" else "Medium",
        "active_subscription_drain": len(subscriptions) > 0
    }

    smart_alert_triggers = []
    for pattern in patterns:
        if pattern["severity"] in ["Medium", "High"]:
            smart_alert_triggers.append({
                "alert_type": pattern["pattern_type"],
                "urgency": "Immediate" if pattern["severity"] == "High" else "Digest",
                "message": pattern["description"]
            })

    return {
        "patterns": patterns,
        "classification": classification,
        "downstream_payloads": {
            "financial_stress_score_engine": financial_stress_indicators,
            "financial_personality_dna_engine": financial_personality_markers,
            "smart_alert_system": smart_alert_triggers
        }
    }
