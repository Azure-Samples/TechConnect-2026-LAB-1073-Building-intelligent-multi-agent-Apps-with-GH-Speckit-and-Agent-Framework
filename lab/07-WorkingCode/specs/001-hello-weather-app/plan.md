# Implementation Plan: HelloWeather Web App

**Branch**: `001-hello-weather-app` | **Date**: 2026-01-10 | **Spec**: [specs/001-hello-weather-app/spec.md](specs/001-hello-weather-app/spec.md)
**Input**: Functional specification describing the HelloWeather single-page web experience with concurrent WeatherAgent + CityAgent orchestration.

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deliver a beginner-friendly FastAPI experience that greets the user, validates a one-sentence self introduction containing a city, and then orchestrates WeatherAgent and CityAgent concurrently through Microsoft Agent Framework. Stream intermediate agent updates to the browser, aggregate the final insights into a ≤60-word combined tip, and always append the constitutional disclaimer while gracefully noting any agent failures.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11 (local dev uses 3.11.7 via .venv)  
**Primary Dependencies**: Microsoft Agent Framework (`agent-framework` pre-release), FastAPI, Uvicorn, Jinja2, python-dotenv, azure-identity (AzureCliCredential fallback).  
**Storage**: N/A (session data held in-memory per request).  
**Testing**: pytest + httpx AsyncClient for API tests with Agent Framework `MockLLM` + stub streaming fixtures.  
**Target Platform**: Cross-platform local dev (Windows/macOS/Linux) running uvicorn.  
**Project Type**: Single web backend with server-rendered template.  
**Performance Goals**: Start streaming within 2 seconds of submission; final combined tip under 60 words.  
**Constraints**: No static weather/city datasets; Azure OpenAI only; must append disclaimer; concurrent execution via ConcurrentBuilder.  
**Scale/Scope**: Single-page demo experience, single session at a time, minimal code footprint (<1k LOC).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Greeting + disclaimer: Plan includes landing copy that prompts for intro + city once, logs acceptance, and injects the exact disclaimer in both stream preamble and final message. ✅
- Parallel orchestration: We will construct a ConcurrentBuilder workflow with WeatherAgent and CityAgent tasks orchestrated via the Agent Framework async run loop. ✅
- Approved stack only: All AI calls go through Azure OpenAI chat completions using Agent Framework clients; no alternate runtimes or SDKs will be introduced. ✅
- No static data: Inputs flow directly to Azure reasoning; validators scrub attempts to rely on cached facts, and tests assert absence of local lookup tables. ✅
- Failure handling: Aggregator design includes explicit degraded-mode branch that emits polite notes when an agent errors or times out while still streaming surviving output. ✅

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/helloweather/
├── __init__.py
├── app.py                 # FastAPI app, routing, streaming responses
├── agents.py              # WeatherAgent, CityAgent definitions
├── orchestration.py       # ConcurrentBuilder workflow + aggregator
├── validators.py          # Input validation and disclaimer utilities
├── telemetry.py           # Logging helpers + structured metrics
└── templates/
  └── index.html         # Single-page form + streamed output area

tests/
├── contract/
│   └── test_aggregator.py # Confirms combined tip + disclaimer contract
├── integration/
│   └── test_streaming.py  # Exercises streaming fan-out/fan-in path
└── unit/
  ├── test_validators.py
  └── test_telemetry.py

docs/
└── quickstart.md          # Generated runtime instructions (Phase 1 output)
```

**Structure Decision**: Single Python package (`src/helloweather`) keeps agents, orchestration, and web app co-located for workshop clarity while separating validation and telemetry for testability. Templates live inside the package to simplify FastAPI `Jinja2Templates` loading. Tests follow contract/integration/unit split to reflect constitutional focus areas.

## Implementation Milestones

1. **Foundation (P1 blocking)**: Scaffold FastAPI app, SSE streaming plumbing, and dotenv/Azure credential wiring; stand up ConcurrentBuilder skeleton with placeholder agents and aggregator returning mock data.
2. **Agent Streams (aligns with User Story 2)**: Implement WeatherAgent and CityAgent prompts, configure `MockLLM` fixtures, and ensure concurrent streaming with live progress telemetry.
3. **Aggregation & Resilience (aligns with User Story 3)**: Finalize deduplication, word-count guardrail, disclaimer injection, and polite degradation handling; add structured logging + metrics.
4. **Validation & Polish (cross-cutting)**: Harden input validators, write pytest coverage across unit/contract/integration layers, and document quickstart plus env requirements.

## Testing Strategy

- **Unit**: Validate `validators.py` sentence+city checks, aggregation dedup logic, and telemetry formatting using pure functions.
- **Contract**: Assert aggregator output structure (≤60 words, disclaimer appended, degradation note semantics) using `MockLLM` scripted runs.
- **Integration**: Exercise FastAPI streaming endpoint with httpx AsyncClient, iterating SSE events to verify concurrent agent updates and failure modes.
- **Tooling**: pytest, pytest-asyncio, coverage (≥80%) focused on orchestration + aggregator modules.

## Observability & Resilience

- Emit structured logs (JSON) with fields: `agent`, `event`, `elapsed_ms`, `status`, `degraded`.
- Capture concurrent task timings via `asyncio.Task` instrumentation to verify fan-out/fan-in in logs.
- Apply per-agent timeouts (default 12s) with single retry before marking degraded; aggregator communicates failure note.
- SSE heartbeat events every 5 seconds prevent browser timeouts and surface idle periods transparently.

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Agent Framework streaming API shifts (pre-release) | Breaks concurrent flow | Pin exact `agent-framework` version and add smoke test in CI |
| SSE disconnect mid-stream | User misses final tip | Detect client disconnect via response callback; cancel tasks, log, and present retry prompt |
| Input lacks reliable city mention | Agents give vague output | Add regex-based city check and request resubmission if unclear |
| Word-count guard trims meaning | Final tip loses clarity | Generate sentences first, measure word count, and rephrase if >60 words before sending |

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
