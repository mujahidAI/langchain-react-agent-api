# LangChain ReAct Agent API

Production-ready FastAPI service exposing a LangChain ReAct agent backed by Groq (LLaMA 3.3 70B) with Tavily web search, calculator, and datetime tools. The API returns both the final answer and the full reasoning trace (Thought → Action → Observation).

## Features
- Groq-hosted LLaMA 3.3 70B with configurable `model_name`, `temperature`, and `max_iterations`.
- ReAct reasoning loop with intermediate tool calls included in responses.
- Three built-in tools: Tavily web search, calculator, current datetime.
- Clean FastAPI architecture: routers, services, schemas, tools as separate modules.
- Dependency management via `uv`; Python 3.10+; dotenv-based configuration.
- Health probe endpoint for readiness checks.

## Folder Structure
```
.
├─ services/           # agent service, prompt loading, tool wiring
├─ services/tools/     # tavily search, calculator, datetime tools
├─ routers/            # FastAPI route definitions
├─ schemas/            # Pydantic request/response models
├─ main.py             # FastAPI app factory / entrypoint
├─ react_prompt.txt    # ReAct prompt template
├─ .env.example        # sample environment variables
└─ README.md
```

## Setup (uv)
```bash
# install dependencies (dev group includes black/linters if present)
uv sync --group dev

# run the API
uv run fastapi dev main.py        # or: uv run uvicorn main:app --reload
```

## Running with Docker

### Prerequisites
- Docker Desktop installed and running

### Setup
```bash
docker-compose up --build
```

API will be live at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Useful Commands

| Command | Description |
|---|---|
| `docker-compose up --build` | Build and start the container |
| `docker-compose down` | Stop the container |
| `docker-compose logs -f` | View live container logs |
| `docker ps` | See running containers |

## Environment Variables
| Name             | Required | Description                                   | Example    |
|------------------|----------|-----------------------------------------------|------------|
| `GROQ_API_KEY`   | Yes      | Groq API key for LLM access                   | `gsk_...`  |
| `TAVILY_API_KEY` | Yes      | Tavily search API key                         | `tvly_...` |
| `PORT`           | No       | Port for the FastAPI server                   | `8000`     |
| `ENV`            | No       | Environment name (`dev`, `prod`, etc.)        | `dev`      |

## Available Groq Models
- `llama-3.3-70b-versatile` (default)
- `llama-3.3-70b-specdec`
- Any other Groq chat model supported by your account (pass via request).

## API Endpoints
### GET `/health`
- Purpose: readiness/liveness check.
- Response: `{"status": "ok"}`

### POST `/agent/run`
- Purpose: run the ReAct agent over a user query.
- Request body:
  - `query` (string, required)
  - `model_name` (string, optional, default `llama-3.3-70b-versatile`)
  - `temperature` (float, optional, default `0.2`)
  - `max_iterations` (int, optional, default `6`)

Example request:
```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
        "query": "What was the Nasdaq close yesterday and what is 3% of it?",
        "model_name": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "max_iterations": 6
      }'
```

Example response:
```json
{
  "result": "The Nasdaq closed at 16,500 yesterday; 3% is 495.",
  "steps": [
    "Tool: search_web | Input: \"Nasdaq close yesterday\" | Result: ...",
    "Tool: calculator | Input: \"16500 * 0.03\" | Result: 495"
  ]
}
```

## How the ReAct Agent Works
- The prompt enforces the loop: Thought → Action → Action Input → Observation.
- The agent selects among registered tools (Tavily search, calculator, datetime) to gather facts or compute.
- The loop repeats until `Final Answer` or `max_iterations` is reached.
- Intermediate steps are returned so callers can audit which tools were used and why.

## Tests / Lint (if configured)
```bash
uv run pytest          # tests
uv run black .         # formatting
```
