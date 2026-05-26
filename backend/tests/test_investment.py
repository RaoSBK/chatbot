import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_chat_success(client: AsyncClient):
    """
    Test standard educational question returns structured response.
    """
    response = await client.post(
        "/api/v1/investment-assistant/chat",
        json={"message": "What is SIP?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "topic" in data
    assert "response" in data
    assert data["topic"] == "SIP"
    assert "Explanation:" in data["response"]
    assert "Example:" in data["response"]
    assert "Benefits:" in data["response"]
    assert "Risks:" in data["response"]
    assert "Takeaway:" in data["response"]

async def test_chat_contextual_memory(client: AsyncClient):
    """
    Test that session ID enables context-aware conversations.
    - Turn 1: Ask "What is SIP?"
    - Turn 2: Ask "Is it risky?" (using session ID)
    The assistant resolves 'it' to SIP.
    """
    session_id = "test_sess_999"

    # Turn 1
    resp1 = await client.post(
        "/api/v1/investment-assistant/chat",
        json={"message": "What is SIP?", "session_id": session_id}
    )
    assert resp1.status_code == 200
    assert resp1.json()["topic"] == "SIP"

    # Turn 2: contextual query
    resp2 = await client.post(
        "/api/v1/investment-assistant/chat",
        json={"message": "Is it risky?", "session_id": session_id}
    )
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["topic"] == "SIP"
    assert "SIP Risks" in data["response"] or "equity and bond market" in data["response"].lower()

async def test_safety_validation_blocked_inbound(client: AsyncClient):
    """
    Test that queries containing stock advice requests, stock recommendations,
    or guaranteed return queries are immediately blocked by safety validation.
    """
    blocked_queries = [
        "Should I buy Tesla stock?",
        "Tell me which stock in ABC is good to invest in",
        "Give me a guaranteed return of 20% on bonds",
        "investment advice for buying apple shares"
    ]

    for query in blocked_queries:
        response = await client.post(
            "/api/v1/investment-assistant/chat",
            json={"message": query}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "General Security"
        assert data["response"] == "This assistant provides educational information only and not financial advice."

async def test_empty_message_validation(client: AsyncClient):
    """
    Test that Pydantic validation rejects empty requests (422 status code).
    """
    response = await client.post(
        "/api/v1/investment-assistant/chat",
        json={"message": ""}
    )
    assert response.status_code == 422
