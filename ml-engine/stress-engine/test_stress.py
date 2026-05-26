import pytest
from fastapi.testclient import TestClient

from inference import app
from feature_engineering import engineer_features
from scoring import calculate_weighted_score
from stress_calculator import evaluate_stress
from classifier import FinancialStressClassifier

client = TestClient(app)

# ----------------------------------------------------
# 1. TARGET CALIBRATED TEST LOGS
# ----------------------------------------------------
def get_example_payload():
    """Returns the exact raw payload provided in the project prompt requirements."""
    return {
        "user_id": "test_user_stress_73",
        "monthly_income": 30000,
        "monthly_expenses": 25000,
        "savings": 3000,
        "goal_progress": 40,
        "weekend_ratio": 1.42,
        "impulse_score": 0.67,
        "spending_volatility": 0.58,
        "subscription_count": 5,
        "budget_utilization": 92,
        "category_spikes": 3
    }

# ----------------------------------------------------
# 2. UNIT TESTS
# ----------------------------------------------------
def test_stress_feature_engineering():
    """Verify raw input metrics map to correct mathematical features."""
    raw = get_example_payload()
    feats = engineer_features(raw)
    
    assert feats["savings_rate"] == 3000 / 30000 # 0.10
    assert feats["budget_pressure"] == 0.92
    assert feats["goal_health_score"] == 0.40
    assert feats["subscription_burden"] == 5.0
    assert feats["category_risk"] == 3.0

def test_stress_scoring_calculations():
    """Verify the weighted scoring calculations remain bound and logically sound."""
    raw = get_example_payload()
    feats = engineer_features(raw)
    score = calculate_weighted_score(feats)
    
    assert 0.0 <= score <= 100.0

def test_stress_classifier_loading():
    """Verify that ML regressor successfully predicts values and handles fallback."""
    classifier = FinancialStressClassifier()
    raw = get_example_payload()
    feats = engineer_features(raw)
    
    predicted_score = classifier.predict_score(feats)
    assert 0.0 <= predicted_score <= 100.0

def test_stress_calibration_exact():
    """Verify that calling evaluate_stress with the target example payload returns exactly 73 (Stable)."""
    raw = get_example_payload()
    report = evaluate_stress(raw)
    
    assert report["stress_score"] == 73
    assert report["stress_level"] == "Stable"
    assert report["confidence"] == 0.91
    assert "High budget utilization" in report["risk_factors"]
    assert "Impulse spending" in report["risk_factors"]
    assert "Reduce discretionary expenses" in report["recommendations"]
    assert "Increase emergency savings" in report["recommendations"]

# ----------------------------------------------------
# 3. API INTEGRATION TESTS
# ----------------------------------------------------
def test_api_analyze_stress():
    """Verify POST /stress/analyze takes request and returns target StressResponse schema."""
    payload = get_example_payload()
    response = client.post("/stress/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["stress_score"] == 73
    assert data["stress_level"] == "Stable"
    assert isinstance(data["risk_factors"], list)
    assert len(data["risk_factors"]) >= 2

def test_api_trends_and_summaries():
    """Verify GET /stress/summary returns the visualization summary, trend, and history."""
    user_id = "user_visual_999"
    
    # 1. First analysis (baseline, Stable trend)
    payload1 = get_example_payload()
    payload1["user_id"] = user_id
    payload1["monthly_expenses"] = 28000.0 # higher expenses (higher stress -> lower score)
    resp1 = client.post("/stress/analyze", json=payload1)
    assert resp1.status_code == 200
    score1 = resp1.json()["stress_score"]
    
    # Check baseline summary
    sum_resp1 = client.get(f"/stress/summary?user_id={user_id}")
    assert sum_resp1.status_code == 200
    assert sum_resp1.json()["trend"] == "Stable"
    
    # 2. Second analysis (improved parameters -> lower stress -> higher score -> Improving trend)
    payload2 = get_example_payload()
    payload2["user_id"] = user_id
    payload2["budget_utilization"] = 45.0   # lower budget pressure
    payload2["impulse_score"] = 0.20        # lower impulse spending
    payload2["savings"] = 9000.0            # higher savings
    resp2 = client.post("/stress/analyze", json=payload2)
    assert resp2.status_code == 200
    
    # Check improving trend summary
    sum_resp2 = client.get(f"/stress/summary?user_id={user_id}")
    assert sum_resp2.status_code == 200
    data = sum_resp2.json()
    assert data["trend"] == "Improving"
    assert data["gauge_score"] > score1

def test_api_validation_errors():
    """Verify validation triggers 422 for invalid parameters (e.g. negative income or values > bounds)."""
    payload = get_example_payload()
    payload["monthly_income"] = -10.0 # Invalid negative income
    
    response = client.post("/stress/analyze", json=payload)
    assert response.status_code == 422
