---

description: "Task list template for feature implementation"
---

# Tasks: HelloWeather Web App

**Input**: Design documents from `/specs/001-hello-weather-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and baseline tooling so downstream phases comply with the constitution.

- [ ] T001 Create src/helloweather package, templates directory, and initial FastAPI entrypoint in src/helloweather/app.py
- [ ] T002 Install and lock dependencies (agent-framework --pre, fastapi, uvicorn, jinja2, python-dotenv, azure-identity, httpx, pytest, pytest-asyncio) in pyproject.toml or requirements.txt
- [ ] T003 [P] Add .env.example with Azure OpenAI variables and define DISCLAIMER constant in src/helloweather/constants.py
- [ ] T004 [P] Configure project-level lint/test scripts (e.g., tasks.json or make target) referencing pytest and uvicorn commands

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [ ] T005 Establish Pydantic models SessionContext, AgentResultEnvelope, StreamEvent, AggregatedTip in src/helloweather/models.py
- [ ] T006 Build validation helpers for single-sentence intro + city extraction in src/helloweather/validators.py
- [ ] T007 Implement telemetry helpers emitting structured JSON logs in src/helloweather/telemetry.py
- [ ] T008 Scaffold ConcurrentBuilder workflow and SSE streaming pipeline with placeholder agents in src/helloweather/orchestration.py
- [ ] T009 [P] Implement aggregator skeleton that merges envelopes, deduplicates sentences, and appends disclaimer (placeholder content) in src/helloweather/orchestration.py
- [ ] T010 [P] Wire FastAPI routes for GET / and POST /api/session returning dummy SSE events in src/helloweather/app.py

**Checkpoint**: Foundation ready—User Story implementation can start in parallel.

---

## Phase 3: User Story 1 - Collect Friendly Inputs (Priority: P1) 🎯 MVP

**Goal**: Users submit a validated one-sentence introduction containing their city and see acknowledgment that guidance is approximate.

**Independent Test**: Run FastAPI TestClient against POST /api/session with valid/invalid payloads; confirm validation errors block orchestration, and successful submissions emit initial system stream events with disclaimer text.

### Implementation

- [ ] T011 [P] [US1] Implement HTML template with intro form and disclaimer banner in src/helloweather/templates/index.html
- [ ] T012 [US1] Finalize GET / handler returning template and exposing validation hints in src/helloweather/app.py
- [ ] T013 [US1] Integrate validators into POST /api/session, returning 422 with user-friendly JSON on failure in src/helloweather/app.py
- [ ] T014 [US1] Emit initial SSE system event acknowledging approximate guidance before agent fan-out in src/helloweather/app.py
- [ ] T015 [US1] Add unit tests for validators (sentence + city detection) in tests/unit/test_validators.py

**Checkpoint**: User Story 1 independently delivers validated input flow with disclaimer; orchestration can remain mocked.

---

## Phase 4: User Story 2 - Watch Agents Stream (Priority: P2)

**Goal**: WeatherAgent and CityAgent run concurrently and stream progress updates to the browser using deterministic mocks in tests.

**Independent Test**: Use pytest-asyncio + httpx AsyncClient with MockLLM to simulate agent responses; assert streamed events include alternating agent labels, heartbeats, and polite delay notices.

### Tests

- [ ] T016 [P] [US2] Create pytest fixture providing Agent Framework MockLLM scripted outputs in tests/conftest.py
- [ ] T017 [P] [US2] Add integration test covering concurrent SSE stream in tests/integration/test_streaming.py

### Implementation

- [ ] T018 [P] [US2] Implement WeatherAgent prompt + system message enforcing truthful approximations in src/helloweather/agents.py
- [ ] T019 [P] [US2] Implement CityAgent prompt + safety guardrails in src/helloweather/agents.py
- [ ] T020 [US2] Configure ConcurrentBuilder to launch both agents with shared SessionContext in src/helloweather/orchestration.py
- [ ] T021 [US2] Implement SSE streaming loop in src/helloweather/app.py consuming run_stream events and emitting labeled updates
- [ ] T022 [US2] Add heartbeat handling and polite waiting notes when one agent lags in src/helloweather/orchestration.py
- [ ] T023 [US2] Log per-agent lifecycle events using telemetry helpers in src/helloweather/telemetry.py

**Checkpoint**: User Story 2 independently demonstrates parallel streaming with deterministic tests.

---

## Phase 5: User Story 3 - Receive Combined Tip (Priority: P3)

**Goal**: Aggregator composes the final ≤60-word combined tip, notes degraded agents, and appends the mandatory disclaimer.

**Independent Test**: Script MockLLM runs where both agents succeed, one degrades, and both fail; assert final SSE event content, word count, and polite messaging match requirements.

### Tests

- [ ] T024 [P] [US3] Add contract test for AggregatedTip builder covering success and degraded scenarios in tests/contract/test_aggregator.py
- [ ] T025 [P] [US3] Extend integration test to assert final SSE event structure in tests/integration/test_streaming.py

### Implementation

- [ ] T026 [P] [US3] Finalize aggregation logic combining AgentResultEnvelopes, deduplicating, and computing word counts in src/helloweather/orchestration.py
- [ ] T027 [US3] Implement polite degradation note injection when any envelope status != success in src/helloweather/orchestration.py
- [ ] T028 [US3] Emit final SSE event with AggregatedTip content and disclaimer in src/helloweather/app.py
- [ ] T029 [US3] Enforce runtime guard preventing >60 words; if exceeded, rephrase via fallback template in src/helloweather/orchestration.py

**Checkpoint**: User Story 3 adds independently testable aggregation behavior and graceful degradation handling.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T030 [P] Document setup, env vars, and streaming demo in README.md referencing quickstart.md
- [ ] T031 Add quick CLI command samples (uvicorn, pytest) to README.md and verify quickstart.md steps
- [ ] T032 [P] Add telemetry unit tests ensuring JSON structure and monotonic elapsed times in tests/unit/test_telemetry.py
- [ ] T033 Conduct manual run with live Azure credentials, capture screenshots/log samples for docs, and verify no static data usage

---

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → User Story 1 (Phase 3) → User Story 2 (Phase 4) → User Story 3 (Phase 5) → Polish (Phase 6).
- Each story depends on completion of prior phases but remains independently testable once its tasks finish.
- Parallel tasks marked [P] can be executed concurrently (e.g., dependency installation while preparing .env template, or parallel pytest fixtures and agent implementations).

## User Story Dependency Graph

- US1 (Collect Friendly Inputs) → US2 (Watch Agents Stream)
- US1 + US2 → US3 (Receive Combined Tip)

## Parallel Execution Examples

- During Phase 2, T005 and T006 can proceed in parallel while T008 sets up orchestration scaffold.
- For US2, implement WeatherAgent (T018) and CityAgent (T019) concurrently, then wire them together (T020).
- For US3, contract test (T024) can be authored in parallel with aggregation logic (T026) before integrating final SSE output (T028).

## Implementation Strategy

- Deliver MVP by completing Phases 1–3 to collect validated inputs and show mock acknowledgement stream.
- Add real concurrent streaming in Phase 4, then finalize aggregation and degradation handling in Phase 5.
- Polish documentation, telemetry tests, and manual validation in Phase 6.
