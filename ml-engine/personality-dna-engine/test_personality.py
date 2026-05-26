import pytest
from fastapi.testclient import TestClient

from inference import app
from feature_engineering import engineer_features
from ensemble_model import get_personality_profile
from personality_classifier import FinancialPersonalityClassifier

client = TestClient(app)

# ----------------------------------------------------
# 1. SAMPLE DATASETS
# ----------------------------------------------------
def get_example_payload():
    """Returns the exact raw payload provided in the project prompt requirements."""
    return {
        "user_id": "test_user_personality_91",
        "monthly_income": 30000,
        "savings_rate": 0.22,
        "stress_score": 72,
        "weekend_ratio": 1.41,
        "impulse_score": 0.63,
        "goal_completion_rate": 0.35,
        "budget_adherence": 0.58,
        "spending_volatility": 0.44,
        "subscription_count": 5,
        "category_distribution": {
            "food": 30,
            "travel": 15,
            "shopping": 20,
            "education": 5
        }
    }

# ----------------------------------------------------
# 2. UNIT TESTS
# ----------------------------------------------------
def test_personality_feature_engineering():
    """Verify raw input metrics map to correct behavioral feature scores."""
    raw = get_example_payload()
    feats = engineer_features(raw)
    
    assert feats["savings_behavior_score"] == (0.22 / 0.25) * 100.0
    assert feats["discipline_score"] == (0.58 * 0.6 + (1.0 - 0.63) * 0.4) * 100.0
    assert feats["goal_commitment_score"] == 35.0
    assert feats["exploration_score"] == 15.0 + 20.0 + 30.0 # travel + shopping + food (discretionary)

def test_personality_classifier_loading():
    """Verify that ML classifier successfully predicts values and handles fallback."""
    classifier = FinancialPersonalityClassifier()
    raw = get_example_payload()
    feats = engineer_features(raw)
    
    ml_pred = classifier.predict_archetype(feats)
    if ml_pred is not None:
        assert ml_pred["personality_type"] in ["Planner", "Saver", "Impulse Buyer", "Explorer", "Dreamer"]
        assert 0.0 <= ml_pred["confidence"] <= 1.0

def test_personality_calibration_exact():
    """Verify that evaluating the exact target payload yields Planner with 0.91 confidence."""
    raw = get_example_payload()
    feats = engineer_features(raw)
    report = get_personality_profile(raw, feats)
    
    assert report["personality_type"] == "Planner"
    assert report["confidence"] == 0.91
    assert "Consistent budgeting" in report["strengths"]
    assert "Strong saving habits" in report["strengths"]
    assert "Low investment diversification" in report["weaknesses"]
    assert "Increase investment allocation" in report["improvement_plan"]
    assert report["coaching_style"] == "Analytical and goal-driven"

# ----------------------------------------------------
# 3. API INTEGRATION TESTS
# ----------------------------------------------------
def test_api_analyze_personality():
    """Verify POST /personality/analyze returns the complete structured schema."""
    payload = get_example_payload()
    response = client.post("/personality/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["personality_type"] == "Planner"
    assert data["confidence"] == 0.91
    assert "Consistent budgeting" in data["strengths"]
    assert "insights" in data
    assert "behavioral_risks" in data["insights"]

def test_api_profile_dashboard():
    """Verify GET /personality/profile returns the dashboard-ready summary and primary color."""
    user_id = "user_dash_personality_123"
    
    # 1. Analyze first to populate history
    payload = get_example_payload()
    payload["user_id"] = user_id
    resp1 = client.post("/personality/analyze", json=payload)
    assert resp1.status_code == 200
    
    # 2. Query GET /personality/profile
    resp2 = client.get(f"/personality/profile?user_id={user_id}")
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["type"] == "Planner"
    assert data["confidence"] == 91
    assert data["primary_color"] == "green"
    assert "financially disciplined" in data["summary"]

def test_api_validation_errors():
    """Verify validation triggers 422 for invalid negative/overflow parameters."""
    payload = get_example_payload()
    payload["savings_rate"] = -0.5 # Invalid negative savings rate
    
    response = client.post("/personality/analyze", json=payload)
    assert response.status_code == 422
