import pytest
from fastapi.testclient import TestClient

from inference import app
from feature_engineering import engineer_features
from pattern_detector import detect_patterns
from classifier import SpendingPatternClassifier

client = TestClient(app)

# ----------------------------------------------------
# 1. SAMPLE DATASETS FOR TESTING
# ----------------------------------------------------
def get_sample_saver_transactions():
    """Generates sample transactions reflecting a highly disciplined saver."""
    return [
        {"amount": "100.00", "category": "Groceries", "date": "2026-03-01", "description": "Grocery"},
        {"amount": "150.00", "category": "Utilities", "date": "2026-03-02", "description": "Electric bill"},
        {"amount": "50.00", "category": "Food", "date": "2026-03-03", "description": "Lunch"},
        {"amount": "120.00", "category": "Transport", "date": "2026-03-04", "description": "Fuel"},
        {"amount": "80.00", "category": "Groceries", "date": "2026-03-05", "description": "Grocery"}
    ]

def get_sample_impulse_transactions():
    """Generates sample transactions reflecting an impulse spender (high weekends, late-nights, spikes)."""
    txs = []
    # Weekday baseline (low spend)
    for day in [2, 3, 4]:
        txs.append({"amount": "200.00", "category": "Rent", "date": f"2026-03-0{day}", "description": "Commute"})
    
    # Salary day spike (1st to 3rd of the month)
    txs.append({"amount": "5000.00", "category": "Shopping", "date": "2026-03-01", "description": "Luxury apparel"})
    txs.append({"amount": "3000.00", "category": "Entertainment", "date": "2026-03-02", "description": "Playstation games"})
    
    # Weekend overspending (Saturday 7th, Sunday 8th)
    txs.append({"amount": "4000.00", "category": "Food", "date": "2026-03-07", "description": "Expensive dining club"})
    txs.append({"amount": "4500.00", "category": "Entertainment", "date": "2026-03-08", "description": "Concert ticket"})
    
    # Recurring Subscription
    txs.append({"amount": "199.00", "category": "Entertainment", "date": "2026-03-05", "description": "Netflix Subscription"})
    txs.append({"amount": "199.00", "category": "Entertainment", "date": "2026-04-05", "description": "Netflix Subscription"})
    
    return txs

# ----------------------------------------------------
# 2. UNIT TESTS
# ----------------------------------------------------
def test_feature_engineering_saver():
    """Verify savers obtain low volatility, low ratios, and low impulse scores."""
    txs = get_sample_saver_transactions()
    feats = engineer_features(txs)
    
    assert feats["average_transaction_value"] == 100.00
    assert feats["daily_spending"] == 100.00
    assert feats["weekend_ratio"] == 0.0 # No weekend transactions in saver log
    assert feats["impulse_score"] < 0.30
    assert feats["subscription_count"] == 0

def test_feature_engineering_impulse():
    """Verify impulse spenders obtain high volatility, weekend overspending, and elevated impulse scores."""
    txs = get_sample_impulse_transactions()
    feats = engineer_features(txs)
    
    assert feats["weekend_ratio"] > 0.30
    assert feats["impulse_score"] > 0.50
    assert feats["subscription_count"] >= 1

def test_pattern_detection_triggers():
    """Verify specific rules (Weekend, Salary, Subscriptions) trigger appropriately."""
    txs = get_sample_impulse_transactions()
    feats = engineer_features(txs)
    patterns = detect_patterns(txs, feats)
    
    pattern_types = [p["pattern_type"] for p in patterns]
    assert "Weekend Overspending" in pattern_types
    assert "Salary-Day Spending Spike" in pattern_types
    assert "Subscription Detection" in pattern_types
    assert "Unusual Expense Detection" in pattern_types

def test_ml_classifier():
    """Verify Saver and Impulse profiles are predicted accurately by the classifier."""
    classifier = SpendingPatternClassifier()
    
    saver_feats = engineer_features(get_sample_saver_transactions())
    saver_pred = classifier.predict_profile(saver_feats)
    assert saver_pred["profile_class"] == "Disciplined Saver"
    
    impulse_feats = engineer_features(get_sample_impulse_transactions())
    impulse_pred = classifier.predict_profile(impulse_feats)
    assert impulse_pred["profile_class"] == "Impulse Spender"

# ----------------------------------------------------
# 3. API INTEGRATION TESTS
# ----------------------------------------------------
def test_api_analyze_endpoint():
    """Verify POST /patterns/analyze takes payload, executes pipeline, and returns target structure."""
    payload = {
        "user_id": "999",
        "transactions": [
            {
                "amount": 4200.00,
                "category": "Food",
                "date": "2026-03-07",
                "description": "Zomato premium delivery late night"
            },
            {
                "amount": 4500.00,
                "category": "Entertainment",
                "date": "2026-03-08",
                "description": "Pub party"
            },
            {
                "amount": 200.00,
                "category": "Transport",
                "date": "2026-03-09",
                "description": "Uber Cab"
            }
        ]
    }
    
    response = client.post("/patterns/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "patterns" in data
    assert isinstance(data["patterns"], list)
    
    # Locate weekend overspending
    weekend = next((p for p in data["patterns"] if p["pattern_type"] == "Weekend Overspending"), None)
    assert weekend is not None
    assert weekend["severity"] == "High"
    assert "User spends" in weekend["description"]

def test_api_history_and_summary_endpoints():
    """Verify history and summary endpoints return correct profiles, alerts, and summaries."""
    user_id = "user_abc_777"
    payload = {
        "user_id": user_id,
        "transactions": get_sample_impulse_transactions()
    }
    
    # 1. Analyze first to populate history
    analyze_resp = client.post("/patterns/analyze", json=payload)
    assert analyze_resp.status_code == 200
    
    # 2. Test GET /patterns/history
    hist_resp = client.get(f"/patterns/history?user_id={user_id}")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert hist_data["user_id"] == user_id
    assert hist_data["history_count"] == 1
    assert "downstream_payloads" in hist_data["history"][0]
    
    # 3. Test GET /patterns/summary
    sum_resp = client.get(f"/patterns/summary?user_id={user_id}")
    assert sum_resp.status_code == 200
    sum_data = sum_resp.json()
    assert sum_data["user_id"] == user_id
    assert sum_data["profile"] == "Impulse Spender"
    assert sum_data["total_patterns_detected"] >= 3
    assert len(sum_data["high_severity_alerts"]) >= 1
