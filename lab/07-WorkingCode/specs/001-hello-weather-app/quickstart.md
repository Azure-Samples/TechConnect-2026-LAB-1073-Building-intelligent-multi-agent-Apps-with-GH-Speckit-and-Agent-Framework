# Quickstart — HelloWeather Web App

## Prerequisites
- Python 3.11 installed locally.
- Azure subscription with Azure OpenAI resource and deployment configured.
- `agent-framework` pre-release package available (use `pip install agent-framework --pre`).
- Ability to authenticate via Azure CLI **or** possess an Azure OpenAI API key.

## 1. Clone & Create Virtual Environment
```bash
python -m venv .venv
.venv/Scripts/activate      # Windows PowerShell
source .venv/bin/activate   # macOS/Linux
pip install --upgrade pip
```

## 2. Install Dependencies
```bash
pip install agent-framework --pre fastapi uvicorn jinja2 python-dotenv azure-identity httpx pytest pytest-asyncio
```

## 3. Configure Environment Variables
Create a `.env` file in the repository root:
```
AZURE_OPENAI_ENDPOINT=YOUR_ENDPOINT
AZURE_OPENAI_DEPLOYMENT=YOUR_CHAT_DEPLOYMENT
AZURE_OPENAI_API_VERSION=2024-05-01-preview
# Optional: uncomment to bypass Azure CLI credential fallback
# AZURE_OPENAI_API_KEY=YOUR_API_KEY
```
Authenticate with Azure CLI if you plan to use `AzureCliCredential`:
```bash
az login
```

## 4. Run the App Locally
```bash
uvicorn helloweather.app:app --reload
```
Open http://127.0.0.1:8000 in a browser. Submit a one-sentence introduction containing your city and watch the live stream of agent updates.

## 5. Run Tests
```bash
pytest
```
Key suites:
- Unit tests (validation + aggregator)
- Contract tests (combined tip + disclaimer)
- Integration tests (SSE streaming with MockLLM)

## 6. Troubleshooting
- **No stream appears**: check browser console; verify SSE supported and server logs show streaming events.
- **Agent fails immediately**: ensure Azure credentials are valid; tests use MockLLM but live runs require Azure OpenAI access.
- **Word count exceeded**: inspect aggregator logs; adjust prompt language or fallback template.
- **Accidental live Azure calls during tests**: tests fail fast if real transport invoked; confirm `MockLLM` fixtures loaded.
