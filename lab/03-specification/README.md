# 03 — Specification

## Specification Overview

In GitHub Spec Kit, the specification captures the user journeys and functional rules that drive the plan, tasks, and implementation phases. It translates the constitution’s guardrails into testable product behaviors without dipping into low-level code or file structure details.

## Specification Contents

- User journeys and scenarios that describe the end-to-end experience.
- Functional requirements tied to those journeys.
- Constraints inherited from the constitution (data sources, tone, safety, concurrency).
- Success criteria that can be validated through manual or automated tests.
- Assumptions and open questions that shape downstream planning.

## Step 1: Generate the Specification with GitHub Copilot:

- [ ] In the VS Code workspace you opened during the constitution phase, confirm GitHub Copilot and GitHub Copilot Chat remain enabled.
- [ ] Open the Copilot Chat panel (sidebar icon or `Ctrl+Alt+Shift+I`).
- [ ] Paste the template prompt below (it includes `/speckit.specify`) and adapt the TODO placeholders to match your project.
- [ ] Hit **Enter** in Github Copilot to draft `spec.md`.

    ![SpecKit](.\Images\1.png)

### Copilot Prompt Template (Copy/Paste in Copilot)

```text
/speckit.specify
# Functional Specification — HelloWeather

## Overview
A minimal web app (FastAPI + HTML form) that asks for a one-sentence self-introduction including a city. On submit, a coordinator triggers concurrent runs of WeatherAgent and CityAgent using Microsoft Agent Framework. The app streams agent status and returns a single combined tip (weather + city guidance) with a brief disclaimer.

## Key Scenarios

## User Input Rules
- Simple web interface, showing progress at every stage of the user interaction.
- Validate the self introduction as exactly one sentence containing a city.
- Reject submissions that omit the city or exceed one sentence with actionable error messaging.

## Agent Orchestration
- Trigger WeatherAgent and CityAgent concurrently via the Microsoft Agent Framework coordinator.
- Apply timeouts/retries and surface a polite note if one agent fails while still returning the other’s insight.

## Streaming & Aggregation
- Stream intermediate agent status to the UI in real time.
- Aggregate updates into a ≤ ~60-word final tip that merges weather and city guidance.

## Constraints
- No static data or local tables; Azure OpenAI only.
- Friendly, concise tone with the mandatory disclaimer in the final response.
- Must run locally with `uvicorn` while emitting clear logs for demos.

## Success Criteria
- Verified concurrent execution, streaming, and aggregation in telemetry or logs.
- Consistent tone, prompt disclaimer, and adherence to the ≤ ~60-word limit.
- Demonstrates Spec Kit + Agent Framework best practices for “hello world” agent prototypes.
- Workshop facilitators Step 2: demonstrate fan-out/fan-in orchestration and streaming without pre-seeded data.
```
You will required to click on "Keep"/"Allow"/"Continue" in the chat window to as copilot works.

## Step 2: After Generating the Specification

- The generated file appears in `specs\001-hello-weather-app/spec.md`; look in VSCode Explorer for the specific file.

    ![SpecKit](.\Images\2.png)

- Verify user journeys cover input validation, concurrent streaming, and final aggregation.
- Confirm each functional requirement ties back to a constitution principle.
- Check that constraints and success criteria are measurable and free of implementation specifics.
- Regenerate if Copilot introduces static data, external APIs, or long narrative paragraphs.

## Human-in-the-Loop Disclaimer

- Inspect every Copilot-generated scenario, requirement, and metric to ensure they match stakeholder expectations before treating them as canonical.
- **If a requirement seems fishy, loop Copilot back in to rewrite or tighten it before tapping a proctor—Copilot drafted the spec, so it should debug its own plot holes faster than a human can read three more user stories.**
- Track edits and changes to keep track.

## Congratulations

This module is now complete. Proceed to [04-plan](../04-plan/README.md) once the above steps are complete.

## Appendix - Sample Specification Reference (Do Not Copy)
>
> Adapted from 07-WorkingCode/specs/001-hello-weather-app/spec.md. Use this structure, but update priorities, tests, and metrics to match current goals.

### User Story 1 — Collect Friendly Inputs (Priority: P1)

- **Why**: Without validated inputs and expectation setting, no downstream agent orchestration can run and the required disclaimer would be missing.
- **Independent Test**: Launch the form locally, submit valid and invalid inputs, and confirm the UI blocks invalid submissions while logging readiness for orchestration.
- **Acceptance Scenarios**:
  1. Given the landing page is loaded, when the user enters a one-sentence intro containing a city and presses submit, then the app begins orchestration and shows a friendly status banner that reiterates the approximation disclaimer.
  2. Given the user enters an intro that lacks a city or exceeds one sentence, when they press submit, then the form highlights validation errors without calling any agents.

### User Story 2 — Watch Agents Stream (Priority: P2)

- **Why**: Streaming demonstrates the concurrency showcase goal and reassures users that progress is happening even before the final tip is ready.
- **Independent Test**: Trigger orchestration with mocked Azure responses and confirm at least one update from each agent appears in the stream with timestamps and courteous tone.
- **Acceptance Scenarios**:
  1. Given orchestration has started, when WeatherAgent emits intermediate messages, then the UI appends them in real time with clear labeling and without blocking CityAgent updates.
  2. Given CityAgent encounters a transient delay, when the timeout threshold is reached, then the stream shows a polite waiting note while WeatherAgent updates continue.

### User Story 3 — Receive Combined Tip (Priority: P3)

- **Why**: The aggregated output is the primary value proposition, proving fan-out/fan-in orchestration and meeting workshop expectations.
- **Independent Test**: Complete mock runs where both agents succeed, one fails, and both timeout to ensure the aggregator caps word count, removes duplicates, and injects polite notes.
- **Acceptance Scenarios**:
  1. Given both agents succeed, when aggregation completes, then the response contains a single ≤60-word paragraph blending both insights plus the exact disclaimer text.
  2. Given CityAgent fails after retries, when WeatherAgent succeeds, then the final response mentions the city guidance degradation, shares the available weather insight, and still includes the disclaimer.

### Edge Cases

- How does the system handle intros without a clear city or inputs that violate content policies?
- What occurs if streaming fails mid-response or both agents exceed their timeout simultaneously?
- How do we prevent duplicate or contradictory sentences when aggregating near-identical agent outputs?

### Functional Requirements (Sample)

- **FR-001**: System must greet the user, collect a one-sentence self introduction and city, and acknowledge limitations before proceeding.
- **FR-002**: System must orchestrate WeatherAgent and CityAgent concurrently via ConcurrentBuilder and stream intermediate updates to the client.
- **FR-003**: System must generate a single combined tip under ~60 words, append the disclaimer "information is approximate—verify locally before planning," and avoid duplicate details.
- **FR-004**: System must degrade gracefully with a polite note if either agent fails while still delivering available insights.
- **FR-005**: System must rely solely on Azure OpenAI via Microsoft Foundry with no hardcoded datasets or external weather APIs.
- **FR-006**: System must validate that the self introduction is exactly one sentence containing a city name and provide actionable error feedback otherwise.
- **FR-007**: System must begin streaming status updates within 2 seconds of submission and tag each update with its originating agent.
- **FR-008**: System must emit structured logs proving concurrent execution, retry outcomes, and final aggregation decisions whenever the local server processes a session.

### Measurable Success Criteria (Sample)

- **SC-001**: ≥95% of sessions deliver the combined tip in under 60 words and include the required disclaimer.
- **SC-002**: Streaming of at least one agent update begins within 2 seconds of both inputs being submitted.
- **SC-003**: Degradation notice is emitted for 100% of agent failures while still returning available insights.
- **SC-004**: Telemetry confirms zero calls per session to non-Azure OpenAI data sources or static lookup tables.

### Assumptions (Sample)

- Streaming updates appear as a vertically stacked timeline on the single-page form, avoiding complex frontend frameworks.
- Azure OpenAI configuration (deployment names, region, keys) is available via environment variables and injected at runtime.
- Local development server supports live reloading for demos; production hardening (auth, persistence) is out of scope per non-goals.
