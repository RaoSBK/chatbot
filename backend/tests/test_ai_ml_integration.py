import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# ----------------------------------------------------
# 1. PERSONALITY DNA INTEGRATION TESTS
# ----------------------------------------------------
async def test_personality_dna_workflow(client: AsyncClient):
    # Target example payload
    payload = {
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
    
    # Test POST /api/v1/personality/analyze
    resp1 = await client.post("/api/v1/personality/analyze", json=payload)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["personality_type"] == "Planner"
    assert data1["confidence"] == 0.91
    assert "Consistent budgeting" in data1["strengths"]
    assert "insights" in data1
    
    # Test GET /api/v1/personality/profile
    resp2 = await client.get(f"/api/v1/personality/profile?user_id={payload['user_id']}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["type"] == "Planner"
    assert data2["confidence"] == 91
    assert data2["primary_color"] == "green"
    
    # Test GET /api/v1/personality/history
    resp3 = await client.get(f"/api/v1/personality/history?user_id={payload['user_id']}")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["user_id"] == payload["user_id"]
    assert data3["history_count"] == 1

# ----------------------------------------------------
# 2. STRESS SCORE INTEGRATION TESTS
# ----------------------------------------------------
async def test_stress_score_workflow(client: AsyncClient):
    payload = {
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
    
    # Test POST /api/v1/stress/analyze
    resp1 = await client.post("/api/v1/stress/analyze", json=payload)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["stress_score"] == 73
    assert data1["stress_level"] == "Stable"
    assert "High budget utilization" in data1["risk_factors"]
    
    # Test GET /api/v1/stress/summary
    resp2 = await client.get(f"/api/v1/stress/summary?user_id={payload['user_id']}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["gauge_score"] == 73
    assert data2["trend"] == "Stable"
    assert data2["stress_level"] == "Stable"

# ----------------------------------------------------
# 3. SPENDING PATTERN INTEGRATION TESTS
# ----------------------------------------------------
async def test_spending_pattern_workflow(client: AsyncClient):
    payload = {
        "user_id": "user_patterns_999",
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
    
    # Test POST /api/v1/patterns/analyze
    resp1 = await client.post("/api/v1/patterns/analyze", json=payload)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert "patterns" in data1
    assert isinstance(data1["patterns"], list)
    
    weekend = next((p for p in data1["patterns"] if p["pattern_type"] == "Weekend Overspending"), None)
    assert weekend is not None
    assert weekend["severity"] == "High"
    
    # Test GET /api/v1/patterns/summary
    resp2 = await client.get(f"/api/v1/patterns/summary?user_id={payload['user_id']}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["user_id"] == payload["user_id"]
    assert data2["total_patterns_detected"] >= 1
