import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def get_auth_headers(client: AsyncClient, username: str, email: str):
    await client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": "password123"}
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

async def test_create_expense(client: AsyncClient):
    headers = await get_auth_headers(client, "user1", "user1@example.com")
    response = await client.post(
        "/api/v1/expenses",
        json={
            "amount": "45.50",
            "category": "Food",
            "merchant": "Supermarket",
            "description": "Weekly grocery shopping",
            "date": "2026-05-26"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "45.50"
    assert data["category"] == "Food"
    assert data["merchant"] == "Supermarket"
    assert "id" in data

async def test_get_expenses_rls(client: AsyncClient):
    headers_u1 = await get_auth_headers(client, "user1", "user1@example.com")
    headers_u2 = await get_auth_headers(client, "user2", "user2@example.com")

    # Create expense for user1
    resp_u1 = await client.post(
        "/api/v1/expenses",
        json={"amount": "100.00", "category": "Rent", "date": "2026-05-01"},
        headers=headers_u1
    )
    expense_u1_id = resp_u1.json()["id"]

    # Create expense for user2
    await client.post(
        "/api/v1/expenses",
        json={"amount": "20.00", "category": "Coffee", "date": "2026-05-02"},
        headers=headers_u2
    )

    # User 1 gets all: should only see their own expense
    response = await client.get("/api/v1/expenses", headers=headers_u1)
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["amount"] == "100.00"

    # User 2 gets User 1's expense directly: should fail with 404 (due to RLS filtering)
    response_get_direct = await client.get(f"/api/v1/expenses/{expense_u1_id}", headers=headers_u2)
    assert response_get_direct.status_code == 404

    # User 2 tries to update User 1's expense: should fail with 404
    response_update = await client.put(
        f"/api/v1/expenses/{expense_u1_id}",
        json={"amount": "150.00"},
        headers=headers_u2
    )
    assert response_update.status_code == 404

    # User 2 tries to delete User 1's expense: should fail with 404
    response_delete = await client.delete(f"/api/v1/expenses/{expense_u1_id}", headers=headers_u2)
    assert response_delete.status_code == 404

    # User 1 updates successfully
    response_update_ok = await client.put(
        f"/api/v1/expenses/{expense_u1_id}",
        json={"amount": "120.00"},
        headers=headers_u1
    )
    assert response_update_ok.status_code == 200
    assert response_update_ok.json()["amount"] == "120.00"

    # User 1 deletes successfully
    response_delete_ok = await client.delete(f"/api/v1/expenses/{expense_u1_id}", headers=headers_u1)
    assert response_delete_ok.status_code == 200
