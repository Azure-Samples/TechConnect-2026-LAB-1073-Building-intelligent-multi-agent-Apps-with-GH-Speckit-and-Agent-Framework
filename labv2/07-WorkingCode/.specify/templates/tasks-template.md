---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
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

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize Python project skeleton aligned with plan.md structure
- [ ] T002 Install Microsoft Agent Framework, Azure OpenAI Foundry SDKs, and streaming utilities
- [ ] T003 [P] Capture configuration scaffolding for Azure OpenAI credentials and constitutional disclaimer text

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Scaffold ConcurrentBuilder pipeline and streaming transport between agents and web client
- [ ] T005 [P] Implement aggregator skeleton that merges agent envelopes and enforces <60-word limit
- [ ] T006 [P] Configure structured logging and telemetry for agent lifecycle events
- [ ] T007 Codify graceful degradation policy and user-facing polite note template
- [ ] T008 Establish shared SessionContext and AgentResultEnvelope data structures
- [ ] T009 Lock in disclaimer injection utility reusable across stories

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Weather Insight Stream (Priority: P1) 🎯 MVP

**Goal**: WeatherAgent streams approximate weather guidance for the requested city via Azure OpenAI.

**Independent Test**: Simulate a session with mock city input and verify streamed weather updates conclude with valid AgentResultEnvelope data.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for WeatherAgent output envelope in tests/contract/test_weather_agent.py
- [ ] T011 [P] [US1] Integration test for streaming weather updates in tests/integration/test_stream_weather.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Implement WeatherAgent prompt and reasoning flow in src/agents/weather_agent.py
- [ ] T013 [P] [US1] Add weather-specific validation to reinforce truthful approximations
- [ ] T014 [US1] Wire WeatherAgent into ConcurrentBuilder pipeline in src/orchestration/concurrent_builder.py
- [ ] T015 [US1] Stream WeatherAgent updates to client transport in src/web/stream.py
- [ ] T016 [US1] Add polite fallback messaging when WeatherAgent responses are low confidence
- [ ] T017 [US1] Emit structured logs for WeatherAgent lifecycle and token usage

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - City Guidance Stream (Priority: P2)

**Goal**: CityAgent streams localized guidance about transit, neighborhoods, timing, or safety.

**Independent Test**: Provide city input with varying contexts and verify guidance remains concise, safe, and constitutionally compliant.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for CityAgent envelope in tests/contract/test_city_agent.py
- [ ] T019 [P] [US2] Integration test for city guidance stream in tests/integration/test_stream_city.py

### Implementation for User Story 2

- [ ] T020 [P] [US2] Implement CityAgent prompt and reasoning flow in src/agents/city_agent.py
- [ ] T021 [US2] Add guardrails for unsafe or unsupported city inputs in src/agents/city_agent.py
- [ ] T022 [US2] Integrate CityAgent stream with ConcurrentBuilder in src/orchestration/concurrent_builder.py
- [ ] T023 [US2] Surface CityAgent updates through client streaming layer with transparency messaging

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Combined Delivery Experience (Priority: P3)

**Goal**: Aggregator merges agent outputs, emits combined tip under ~60 words, and injects disclaimer/disclaimer-driven transparency.

**Independent Test**: Trigger runs with both successful and failing agents to verify final response formatting, word count, and polite degradation note.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for aggregator envelope in tests/contract/test_aggregator.py
- [ ] T025 [P] [US3] Integration test for combined streaming + final response in tests/integration/test_combined_output.py

### Implementation for User Story 3

- [ ] T026 [P] [US3] Implement aggregator finalization logic in src/orchestration/aggregator.py
- [ ] T027 [US3] Enforce <60-word validation and duplication removal in src/orchestration/aggregator.py
- [ ] T028 [US3] Inject disclaimer and polite degradation note into web response in src/web/response_builder.py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for WeatherAgent output envelope in tests/contract/test_weather_agent.py"
Task: "Integration test for streaming weather updates in tests/integration/test_stream_weather.py"

# Launch WeatherAgent implementation steps together:
Task: "Implement WeatherAgent prompt and reasoning flow in src/agents/weather_agent.py"
Task: "Wire WeatherAgent into ConcurrentBuilder pipeline in src/orchestration/concurrent_builder.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
