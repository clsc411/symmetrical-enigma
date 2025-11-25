"""Tests for the EchoAgent class."""

import pytest

from agents.echo_agent import EchoAgent


class TestEchoAgent:
    """Test cases for EchoAgent."""

    def test_default_init(self) -> None:
        """Test default initialization."""
        agent = EchoAgent()
        assert agent.name == "EchoAgent"
        assert agent.description == "Echoes back the input message"
        assert agent.prefix == ""

    def test_custom_init(self) -> None:
        """Test custom initialization."""
        agent = EchoAgent(
            name="CustomEcho",
            description="Custom echo agent",
            prefix="Echo: ",
        )
        assert agent.name == "CustomEcho"
        assert agent.description == "Custom echo agent"
        assert agent.prefix == "Echo: "

    @pytest.mark.asyncio
    async def test_process_without_prefix(self) -> None:
        """Test processing without a prefix."""
        agent = EchoAgent()
        result = await agent.process("Hello, World!")
        assert result == "Hello, World!"

    @pytest.mark.asyncio
    async def test_process_with_prefix(self) -> None:
        """Test processing with a prefix."""
        agent = EchoAgent(prefix="Echo: ")
        result = await agent.process("Hello, World!")
        assert result == "Echo: Hello, World!"

    @pytest.mark.asyncio
    async def test_process_empty_message(self) -> None:
        """Test processing an empty message."""
        agent = EchoAgent()
        result = await agent.process("")
        assert result == ""
