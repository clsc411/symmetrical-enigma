"""FastAPI application for agent interactions."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents import EchoAgent
from core import BaseAgent

app = FastAPI(
    title="Symmetrical Enigma",
    description="An experimental playground for composable AI agents and tools",
    version="0.1.0",
)


class MessageRequest(BaseModel):
    """Request model for agent messages.

    Attributes:
        message: The message to send to the agent.
    """

    message: str


class MessageResponse(BaseModel):
    """Response model for agent messages.

    Attributes:
        agent_name: The name of the agent that processed the message.
        response: The agent's response to the message.
    """

    agent_name: str
    response: str


class AgentInfo(BaseModel):
    """Model for agent information.

    Attributes:
        name: The agent's name.
        description: A brief description of the agent.
    """

    name: str
    description: str


# Registry of available agents
_agents: dict[str, BaseAgent] = {}


def register_agent(agent: BaseAgent) -> None:
    """Register an agent in the global registry.

    Args:
        agent: The agent to register.
    """
    _agents[agent.name] = agent


def get_agent(name: str) -> BaseAgent | None:
    """Get an agent by name from the registry.

    Args:
        name: The name of the agent to retrieve.

    Returns:
        The agent if found, None otherwise.
    """
    return _agents.get(name)


def list_agents() -> list[BaseAgent]:
    """List all registered agents.

    Returns:
        A list of all registered agents.
    """
    return list(_agents.values())


# Register default agents
register_agent(EchoAgent())


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint.

    Returns:
        A welcome message.
    """
    return {"message": "Welcome to Symmetrical Enigma!"}


@app.get("/agents", response_model=list[AgentInfo])
async def get_agents() -> list[dict[str, str]]:
    """Get a list of all available agents.

    Returns:
        A list of agent information dictionaries.
    """
    return [agent.get_info() for agent in list_agents()]


@app.get("/agents/{agent_name}", response_model=AgentInfo)
async def get_agent_info(agent_name: str) -> dict[str, str]:
    """Get information about a specific agent.

    Args:
        agent_name: The name of the agent.

    Returns:
        Agent information dictionary.

    Raises:
        HTTPException: If the agent is not found.
    """
    agent = get_agent(agent_name)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return agent.get_info()


@app.post("/agents/{agent_name}/process", response_model=MessageResponse)
async def process_message(agent_name: str, request: MessageRequest) -> MessageResponse:
    """Send a message to an agent for processing.

    Args:
        agent_name: The name of the agent to process the message.
        request: The message request.

    Returns:
        The agent's response.

    Raises:
        HTTPException: If the agent is not found.
    """
    agent = get_agent(agent_name)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    response = await agent.process(request.message)
    return MessageResponse(agent_name=agent.name, response=response)
