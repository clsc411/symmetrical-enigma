"""Base agent class for composable AI agents."""

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract base class for all agents.

    This class defines the interface that all agents must implement.
    Agents are composable units that can process messages and return responses.

    Attributes:
        name: A human-readable name for the agent.
        description: A brief description of what the agent does.
    """

    def __init__(self, name: str, description: str = "") -> None:
        """Initialize the base agent.

        Args:
            name: A human-readable name for the agent.
            description: A brief description of what the agent does.
        """
        self.name = name
        self.description = description

    @abstractmethod
    async def process(self, message: str) -> str:
        """Process an incoming message and return a response.

        Args:
            message: The input message to process.

        Returns:
            The agent's response to the message.
        """
        pass

    def get_info(self) -> dict[str, Any]:
        """Get information about this agent.

        Returns:
            A dictionary containing the agent's name and description.
        """
        return {
            "name": self.name,
            "description": self.description,
        }
