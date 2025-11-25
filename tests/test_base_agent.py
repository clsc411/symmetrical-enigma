"""Tests for the BaseAgent class."""

import pytest

from core.base_agent import BaseAgent


class ConcreteAgent(BaseAgent):
    """A concrete implementation of BaseAgent for testing."""

    async def process(self, message: str) -> str:
        """Process a message by returning it uppercase."""
        return message.upper()


class TestBaseAgent:
    """Test cases for BaseAgent."""

    def test_init_with_name_only(self) -> None:
        """Test initialization with only a name."""
        agent = ConcreteAgent(name="TestAgent")
        assert agent.name == "TestAgent"
        assert agent.description == ""

    def test_init_with_description(self) -> None:
        """Test initialization with name and description."""
        agent = ConcreteAgent(name="TestAgent", description="A test agent")
        assert agent.name == "TestAgent"
        assert agent.description == "A test agent"

    def test_get_info(self) -> None:
        """Test getting agent information."""
        agent = ConcreteAgent(name="TestAgent", description="A test agent")
        info = agent.get_info()
        assert info == {"name": "TestAgent", "description": "A test agent"}

    @pytest.mark.asyncio
    async def test_process(self) -> None:
        """Test the process method."""
        agent = ConcreteAgent(name="TestAgent")
        result = await agent.process("hello")
        assert result == "HELLO"
