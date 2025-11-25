"""Echo agent implementation."""

from core.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    """A simple agent that echoes back the input message.

    This agent serves as a basic example and can be used for testing.
    It optionally adds a prefix to the echoed message.

    Attributes:
        prefix: Optional text to prepend to echoed messages.
    """

    def __init__(
        self,
        name: str = "EchoAgent",
        description: str = "Echoes back the input message",
        prefix: str = "",
    ) -> None:
        """Initialize the echo agent.

        Args:
            name: A human-readable name for the agent.
            description: A brief description of what the agent does.
            prefix: Optional text to prepend to echoed messages.
        """
        super().__init__(name=name, description=description)
        self.prefix = prefix

    async def process(self, message: str) -> str:
        """Echo the input message with an optional prefix.

        Args:
            message: The input message to echo.

        Returns:
            The message, optionally prefixed.
        """
        if self.prefix:
            return f"{self.prefix}{message}"
        return message
