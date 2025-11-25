# symmetrical-enigma

Symmetrical Enigma is an experimental playground for composable AI agents, tools, and workflows.

## Project Structure

```
symmetrical-enigma/
├── core/           # Core components (BaseAgent class)
├── agents/         # Agent implementations
├── tools/          # Tool implementations
├── tests/          # Test suite
└── main.py         # FastAPI application
```

## Installation

```bash
pip install -e ".[dev]"
```

## Running the Server

```bash
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - Welcome message
- `GET /agents` - List all registered agents
- `GET /agents/{agent_name}` - Get info about a specific agent
- `POST /agents/{agent_name}/process` - Send a message to an agent

### Example Usage

```bash
# List all agents
curl http://localhost:8000/agents

# Send a message to the EchoAgent
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!"}' \
  http://localhost:8000/agents/EchoAgent/process
```

## Running Tests

```bash
pytest
```

## Creating New Agents

Extend the `BaseAgent` class and implement the `process` method:

```python
from core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="MyAgent", description="My custom agent")
    
    async def process(self, message: str) -> str:
        # Your agent logic here
        return f"Processed: {message}"
```

Then register your agent in `main.py`:

```python
from agents.my_agent import MyAgent

register_agent(MyAgent())
```

