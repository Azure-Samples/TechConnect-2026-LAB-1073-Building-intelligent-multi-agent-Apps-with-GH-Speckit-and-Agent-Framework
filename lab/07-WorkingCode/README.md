# HelloWeather Prototype

HelloWeather is a workshop-friendly Python demo that showcases concurrent Microsoft Agent Framework agents orchestrated through a FastAPI web experience. Users share a one-sentence self introduction that includes their city, then watch WeatherAgent and CityAgent stream updates before receiving a combined tip with the constitutional disclaimer.

## Features

- Azure OpenAI client bootstrap with Azure CLI auth fallback to API key.
- WeatherAgent (1–2 sentence approximate weather tip) and CityAgent (one sentence city guidance) defined as chat agents with no static data.
- Concurrent workflow that streams intermediate updates and aggregates final output into a ≤60-word paragraph + disclaimer.
- FastAPI web UI with streaming updates rendered through Server-Sent Events (processed via Fetch streaming).
- Resilience: per-agent timeouts, single retry, graceful degradation note when an agent fails.

## Prerequisites

- Python 3.11+
- Azure subscription with Azure OpenAI resource + chat deployment
- `agent-framework` pre-release package (GitHub hosted)
- Azure CLI for default authentication (`az login`)

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows PowerShell
source .venv/bin/activate   # macOS/Linux

pip install --upgrade pip
pip install agent-framework --pre fastapi uvicorn jinja2 python-dotenv azure-identity httpx pytest pytest-asyncio
```

Copy `.env` and fill in your values:

```bash
cp .env .env.local  # or edit .env directly
```

```
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE-NAME.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=YOUR_CHAT_DEPLOYMENT_NAME
AZURE_OPENAI_API_VERSION=2024-05-01-preview
# Optional when not using Azure CLI auth
# AZURE_OPENAI_API_KEY=YOUR_KEY
```

Authenticate with Azure CLI if you rely on CLI credentials:

```bash
az login
```

## Run Locally

```bash
uvicorn app:app --reload
```

Open http://127.0.0.1:8000 and submit the form. Progress appears in the timeline; the final paragraph includes "Information is approximate—verify locally before planning."

## Testing

Tests are not included in this minimal prototype, but the code is structured for pytest-based unit, contract, and integration suites (see the `agents.aggregate_agent_outputs` helper and streaming workflow generator).

## Notes

- The prototype prefers the official Microsoft Agent Framework; a lightweight fallback is provided for environments where the package is absent, but the best experience requires the real runtime.
- Avoid placing static weather tables or persistent data in the project—agents rely entirely on Azure OpenAI reasoning.
- Logging output (INFO level) highlights per-agent durations and aggregator timing to help with demos.
