import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_generate_saving_recommendations_food_exact(client: AsyncClient):
    """
    Test recommendation generation with the exact prompt values, demonstrating that
    when food spending is 6000 (which exceeds 35% of total expenses and 20% of monthly income),
    the savings are exactly 1200 and severity is High.
    """
    response = await client.post(
        "/api/v1/recommendations",
        json={
            "monthly_income": 30000,
            "expenses": [
                {
                    "amount": "6000.00",
                    "category": "Food",
                    "date": "2026-03-01",
                    "description": "Weekly groceries and delivery"
                }
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Locate Food Spending recommendation
    food_rec = next((r for r in data if r["recommendation_type"] == "Food Spending"), None)
    assert food_rec is not None
    assert food_rec["severity"] == "High"
    assert float(food_rec["possible_savings"]) == 1200.00
    assert food_rec["confidence"] == 0.92
    assert food_rec["recommendation"] == "Reduce food delivery spending by 20%"
    assert food_rec["reason"] == "Food spending exceeds 35% of total expenses"

async def test_generate_multiple_recommendations(client: AsyncClient):
    """
    Test generating multiple recommendations simultaneously for food, entertainment, and subscriptions.
    """
    response = await client.post(
        "/api/v1/recommendations",
        json={
            "monthly_income": 5000,
            "expenses": [
                {"amount": "2000.00", "category": "Food Delivery", "date": "2026-03-01"},
                {"amount": "800.00", "category": "Leisure & Movies", "date": "2026-03-02"},
                {"amount": "400.00", "category": "Netflix Subscription", "date": "2026-03-03"},
                {"amount": "1000.00", "category": "Rent", "date": "2026-03-04"} # non-matching category
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

    # Check for Food Spending
    food = next(r for r in data if r["recommendation_type"] == "Food Spending")
    assert food["severity"] == "High"
    assert float(food["possible_savings"]) == 400.00 # 20% of 2000
    
    # Check for Entertainment
    ent = next(r for r in data if r["recommendation_type"] == "Entertainment Spending")
    assert float(ent["possible_savings"]) == 240.00 # 30% of 800

    # Check for Subscriptions
    sub = next(r for r in data if r["recommendation_type"] == "Subscription Auditing")
    assert float(sub["possible_savings"]) == 160.00 # 40% of 400

async def test_recommendations_empty_expenses(client: AsyncClient):
    """
    Test with an empty list of expenses.
    """
    response = await client.post(
        "/api/v1/recommendations",
        json={
            "monthly_income": 3000,
            "expenses": []
        }
    )
    assert response.status_code == 200
    assert response.json() == []

async def test_recommendations_invalid_input(client: AsyncClient):
    """
    Test request validation with invalid payloads.
    """
    # Negative income
    response = await client.post(
        "/api/v1/recommendations",
        json={
            "monthly_income": -100,
            "expenses": []
        }
    )
    assert response.status_code == 422

    # Negative expense amount
    response = await client.post(
        "/api/v1/recommendations",
        json={
            "monthly_income": 3000,
            "expenses": [
                {"amount": "-10.00", "category": "Food", "date": "2026-03-01"}
            ]
        }
    )
    assert response.status_code == 422
