"""Tests for the FastAPI application."""

import pytest
from httpx import ASGITransport, AsyncClient

from main import app, register_agent, _agents
from agents.echo_agent import EchoAgent


@pytest.fixture(autouse=True)
def reset_agents() -> None:
    """Reset agents registry before each test."""
    _agents.clear()
    register_agent(EchoAgent())


@pytest.fixture
async def client() -> AsyncClient:
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestRootEndpoint:
    """Test cases for root endpoint."""

    @pytest.mark.asyncio
    async def test_root(self, client: AsyncClient) -> None:
        """Test the root endpoint returns a welcome message."""
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Symmetrical Enigma!"}


class TestAgentsEndpoints:
    """Test cases for agent endpoints."""

    @pytest.mark.asyncio
    async def test_list_agents(self, client: AsyncClient) -> None:
        """Test listing all agents."""
        response = await client.get("/agents")
        assert response.status_code == 200
        agents = response.json()
        assert len(agents) == 1
        assert agents[0]["name"] == "EchoAgent"

    @pytest.mark.asyncio
    async def test_get_agent_info(self, client: AsyncClient) -> None:
        """Test getting info for a specific agent."""
        response = await client.get("/agents/EchoAgent")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "EchoAgent"
        assert data["description"] == "Echoes back the input message"

    @pytest.mark.asyncio
    async def test_get_agent_not_found(self, client: AsyncClient) -> None:
        """Test getting info for a non-existent agent."""
        response = await client.get("/agents/NonExistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestProcessEndpoint:
    """Test cases for the process endpoint."""

    @pytest.mark.asyncio
    async def test_process_message(self, client: AsyncClient) -> None:
        """Test processing a message through an agent."""
        response = await client.post(
            "/agents/EchoAgent/process",
            json={"message": "Hello, World!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["agent_name"] == "EchoAgent"
        assert data["response"] == "Hello, World!"

    @pytest.mark.asyncio
    async def test_process_agent_not_found(self, client: AsyncClient) -> None:
        """Test processing with a non-existent agent."""
        response = await client.post(
            "/agents/NonExistent/process",
            json={"message": "Hello"},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_process_empty_message(self, client: AsyncClient) -> None:
        """Test processing an empty message."""
        response = await client.post(
            "/agents/EchoAgent/process",
            json={"message": ""},
        )
        assert response.status_code == 200
        assert response.json()["response"] == ""
