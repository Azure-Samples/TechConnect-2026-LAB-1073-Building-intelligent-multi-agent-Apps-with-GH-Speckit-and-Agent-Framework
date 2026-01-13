# 04 — Plan

## Planning Overview
In GitHub Spec Kit, the plan turns the specification into a concrete roadmap. It identifies the environment, files, milestones, and risks that guide `/speckit.tasks` and `/speckit.implement`. Think of it as the blueprint you validate before writing code.

## Planning Contents
- Environment and dependency expectations.
- Repository layout and file ownership for the upcoming work.
- Agent orchestration details derived from the specification.
- Web and API behavior checkpoints, including streaming and validation.
- Resilience, observability, and test strategy notes.
- Post-generation review steps and sample structure.

## Generate the Plan with GitHub Copilot
1. In the VS Code workspace you opened during the constitution phase, confirm GitHub Copilot and GitHub Copilot Chat are still enabled and authenticated.
2. Open the Copilot Chat panel (sidebar icon or `Ctrl+Alt+Shift+I`).
3. Paste the prompt template below (it includes `/speckit.plan`) and adapt the TODOs for your project.
4. Ask Copilot to draft `plan.md`. Review the output for alignment with the constitution and specification.
5. Save the refined plan inside `.specify/memory/` and copy critical sections into this README for quick reference.

### Copilot Prompt Template (Copy/Paste in Copilot)
```text
/speckit.plan
# Implementation Plan — HelloWeather

## Goals
- Translate the specification into a workshop-friendly demo.
- Highlight major workstreams for frontend, agents, and orchestration.

## Environment
- Python 3.10 or later.
- Packages: agent-framework --pre, fastapi, uvicorn, jinja2, python-dotenv.
- Auth: Azure CLI preferred with API key fallback.
- Env vars: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION, optional AZURE_OPENAI_API_KEY.

## Project Layout
- app.py — FastAPI endpoints and streaming hook.
- agents.py — WeatherAgent, CityAgent, and orchestrator wiring.
- templates/index.html — form inputs and live status area.
- README.md, .env.example.

## Workstreams
- Setup & scaffolding.
- Agent prompts and concurrency wiring.
- Streaming experience and final aggregation polish.
- Validation, logging, and lightweight tests.

## Milestones
- P1: Environment ready and skeleton runs locally.
- P2: Agents stream updates concurrently with placeholder content.
- P3: Aggregator merges results, adds disclaimer, and handles failures politely.
- P4: Final polish, docs, and demo checklist.

## Risks & Mitigations
- Agent errors → add retry plus fallback messaging.
- Streaming dropout → surface reconnect or retry guidance.
- Validation gaps → enforce intro + city requirement with friendly errors.

## Validation
- Run `uvicorn app:app --reload` locally.
- Test known/unknown cities and invalid intros to confirm no static lookups.
```

## After Generating the Plan
- The generated file appears in `.specify/memory/plan.md`; copy key decisions into this README.
- Verify environment steps match your dev setup (Python version, dependencies, authentication flow).
- Confirm the layout aligns with how you want to organize `app.py`, `agents.py`, and templates.
- Ensure agent design, orchestration, and streaming sections honor specification and constitution constraints.
- Review resilience and validation steps; add or adjust tasks if Copilot misses critical risks.

## Human-in-the-Loop Disclaimer
- Vet every milestone, dependency, and risk in the plan to ensure it reflects reality before sharing it with the team.
- **If a timeline slips or a task looks magical, have GitHub Copilot revise its own roadmap before sounding the alarm—Copilot charted the course, so it should steer the ship faster than explaining detours to your instructor.**
- Record any manual edits so the tasks phase inherits accurate sequencing and ownership notes.

Proceed to [05-tasks](../05-tasks/README.md) once the above steps are complete.

## Sample Plan Reference (Do Not Copy)
> Adapted from 07-WorkingCode/specs/001-hello-weather-app/plan.md. Update paths, metrics, and risks to match your current objectives.

### Summary
Deliver a FastAPI demo that gathers the intro + city input, runs both agents together, streams progress, and ends with one concise tip plus disclaimer.

### Technical Context (High Level)
- Python 3.11 in a virtual environment.
- Core packages: agent-framework (pre-release), fastapi, uvicorn, jinja2, python-dotenv, azure-identity.
- No persistent storage; everything happens per request.

### Project Structure (Sample)
```text
hello-weather-lab/07-WorkingCode/
├── app.py
├── agents.py
├── templates/
│   └── index.html
├── .env.example
└── README.md
```

### Milestones (Sample)
1. Foundation: environment ready, FastAPI skeleton running.
2. Agent Streams: concurrent WeatherAgent + CityAgent updates visible.
3. Aggregation: final tip capped to ~60 words with disclaimer and fallback note.
4. Polish: friendly validation, lightweight tests, and demo instructions.

### Testing & Validation (Sample)
- Manual runs with uvicorn plus a few pytest checks for validators or aggregation.
- Confirm at least one stream event per agent, even when one fails.

### Risks & Mitigations (Sample)
| Risk | Mitigation |
| --- | --- |
| Agent API changes | Pin package version, rerun smoke test |
| Streaming dropout | Show reconnect guidance, allow quick resubmit |
| Missing city in intro | Prompt user to resubmit with a city |

**Version**: _Update when plan is ratified_ | **Reviewed**: _YYYY-MM-DD_
