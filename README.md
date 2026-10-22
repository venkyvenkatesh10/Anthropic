# FirstNet Cosmos Agent Boilerplate

This starter provides a FirstNet-style dashboard, FastAPI API, natural-language query planner, query validator, and Cosmos DB executor.

## Run locally in mock mode

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. Mock mode returns sample incident data without connecting to Cosmos DB or OpenAI.

## Connect real services

Set these values in `.env`:

```text
MOCK_MODE=false
OPENAI_API_KEY=...
COSMOS_ENDPOINT=...
COSMOS_KEY=...
COSMOS_DATABASE=...
COSMOS_CONTAINER=incidents
```

Before production, replace key-based Cosmos authentication with Azure Managed Identity, add user authentication, restrict CORS, add audit logging, and add tests for every approved query pattern.

