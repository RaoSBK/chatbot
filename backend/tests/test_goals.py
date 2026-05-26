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

async def test_create_goal(client: AsyncClient):
    headers = await get_auth_headers(client, "user1", "user1@example.com")
    response = await client.post(
        "/api/v1/goals",
        json={
            "name": "New Car",
            "target_amount": "25000.00",
            "current_amount": "1000.00",
            "target_date": "2027-12-31"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Car"
    assert data["target_amount"] == "25000.00"
    assert data["current_amount"] == "1000.00"
    assert "id" in data

async def test_get_goals_rls(client: AsyncClient):
    headers_u1 = await get_auth_headers(client, "user1", "user1@example.com")
    headers_u2 = await get_auth_headers(client, "user2", "user2@example.com")

    # Create goal for user1
    resp_u1 = await client.post(
        "/api/v1/goals",
        json={"name": "Vacation Fund", "target_amount": "3000.00", "target_date": "2026-09-01"},
        headers=headers_u1
    )
    goal_u1_id = resp_u1.json()["id"]

    # User 2 gets User 1's goal directly: should fail with 404
    response_get_direct = await client.get(f"/api/v1/goals/{goal_u1_id}", headers=headers_u2)
    assert response_get_direct.status_code == 404

    # User 2 tries to update User 1's goal: should fail with 404
    response_update = await client.put(
        f"/api/v1/goals/{goal_u1_id}",
        json={"current_amount": "1500.00"},
        headers=headers_u2
    )
    assert response_update.status_code == 404

    # User 2 tries to delete User 1's goal: should fail with 404
    response_delete = await client.delete(f"/api/v1/goals/{goal_u1_id}", headers=headers_u2)
    assert response_delete.status_code == 404

    # User 1 updates successfully
    response_update_ok = await client.put(
        f"/api/v1/goals/{goal_u1_id}",
        json={"current_amount": "200.00"},
        headers=headers_u1
    )
    assert response_update_ok.status_code == 200
    assert response_update_ok.json()["current_amount"] == "200.00"

    # User 1 deletes successfully
    response_delete_ok = await client.delete(f"/api/v1/goals/{goal_u1_id}", headers=headers_u1)
    assert response_delete_ok.status_code == 200
