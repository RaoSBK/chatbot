import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password_hash" not in data

async def test_register_duplicate_username(client: AsyncClient):
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Second registration with same username
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "other@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

async def test_register_duplicate_email(client: AsyncClient):
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Second registration with same email
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "otheruser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

async def test_login_success(client: AsyncClient):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(client: AsyncClient):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
