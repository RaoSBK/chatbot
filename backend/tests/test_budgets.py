import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def get_auth_headers(client: AsyncClient, full_name: str, email: str):
    await client.post(
        "/api/v1/auth/register",
        json={"full_name": full_name, "email": email, "password": "password123"}
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

async def test_create_budget(client: AsyncClient):
    headers = await get_auth_headers(client, "user1", "user1@example.com")
    response = await client.post(
        "/api/v1/budgets",
        json={
            "category": "Travel",
            "monthly_limit": "500.00"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Travel"
    assert data["monthly_limit"] == "500.00"
    assert "budget_id" in data

async def test_get_budgets_rls(client: AsyncClient):
    headers_u1 = await get_auth_headers(client, "user1", "user1@example.com")
    headers_u2 = await get_auth_headers(client, "user2", "user2@example.com")

    # Create budget for user1
    resp_u1 = await client.post(
        "/api/v1/budgets",
        json={"category": "Groceries", "monthly_limit": "300.00"},
        headers=headers_u1
    )
    budget_u1_id = resp_u1.json()["budget_id"]

    # User 2 gets User 1's budget directly: should fail with 404
    response_get_direct = await client.get(f"/api/v1/budgets/{budget_u1_id}", headers=headers_u2)
    assert response_get_direct.status_code == 404

    # User 2 tries to update User 1's budget: should fail with 404
    response_update = await client.put(
        f"/api/v1/budgets/{budget_u1_id}",
        json={"monthly_limit": "350.00"},
        headers=headers_u2
    )
    assert response_update.status_code == 404

    # User 2 tries to delete User 1's budget: should fail with 404
    response_delete = await client.delete(f"/api/v1/budgets/{budget_u1_id}", headers=headers_u2)
    assert response_delete.status_code == 404

    # User 1 updates successfully
    response_update_ok = await client.put(
        f"/api/v1/budgets/{budget_u1_id}",
        json={"monthly_limit": "400.00"},
        headers=headers_u1
    )
    assert response_update_ok.status_code == 200
    assert response_update_ok.json()["monthly_limit"] == "400.00"

    # User 1 deletes successfully
    response_delete_ok = await client.delete(f"/api/v1/budgets/{budget_u1_id}", headers=headers_u1)
    assert response_delete_ok.status_code == 200
