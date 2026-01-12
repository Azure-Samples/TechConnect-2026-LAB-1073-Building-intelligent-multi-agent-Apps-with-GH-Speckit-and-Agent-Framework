# Feature Specification: HelloWeather Web App

**Feature Branch**: `001-hello-weather-app`  
**Created**: 2026-01-10  
**Status**: Draft  
**Input**: Functional Specification — HelloWeather: minimal web app with a single form that collects a one-sentence self introduction with city, triggers concurrent WeatherAgent and CityAgent runs via Microsoft Agent Framework, streams agent status, aggregates into a single ≤60-word tip with disclaimer, enforces validation, and degrades gracefully on failures.

> Constitution alignment: Document how the feature greets users, collects a one-sentence introduction plus city, streams parallel agent updates, and delivers a single combined tip under ~60 words with the required disclaimer.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Collect Friendly Inputs (Priority: P1)

The visitor lands on HelloWeather, reads a greeting, submits a one-sentence self introduction that includes their city, and acknowledges the approximate nature of the tips.

**Why this priority**: Without validated inputs and expectation setting, no downstream agent orchestration can run and the constitutionally required disclaimer would be missing.

**Independent Test**: Launch the form locally, submit valid and invalid inputs, and confirm the UI blocks invalid submissions while logging readiness for orchestration.

**Acceptance Scenarios**:

1. **Given** the landing page is loaded, **When** the user enters a one-sentence intro containing a city and presses submit, **Then** the app begins orchestration and shows a friendly status banner that reiterates the approximation disclaimer.
2. **Given** the user enters an intro that lacks a city or exceeds one sentence, **When** they press submit, **Then** the form highlights validation errors without calling any agents.

---

### User Story 2 - Watch Agents Stream (Priority: P2)

After submission, the user sees concurrent streaming updates from WeatherAgent and CityAgent that confirm work-in-progress and surface partial insights as they arrive.

**Why this priority**: Streaming demonstrates the concurrency showcase goal and reassures users that progress is happening even before the final tip is ready.

**Independent Test**: Trigger orchestration with mocked Azure responses and confirm at least one update from each agent appears in the stream with timestamps and courteous tone.

**Acceptance Scenarios**:

1. **Given** orchestration has started, **When** WeatherAgent emits intermediate messages, **Then** the UI appends them in real time with clear labeling and without blocking CityAgent updates.
2. **Given** CityAgent encounters a transient delay, **When** the timeout threshold is reached, **Then** the stream shows a polite waiting note while WeatherAgent updates continue.

---

### User Story 3 - Receive Combined Tip (Priority: P3)

Once both agents finish (or one fails gracefully), the user receives a concise combined tip that merges weather and city guidance, acknowledges any degradation, and closes with the mandatory disclaimer.

**Why this priority**: The aggregated output is the primary value proposition, proving fan-out/fan-in orchestration and meeting workshop expectations.

**Independent Test**: Complete mock runs where both agents succeed, one fails, and both timeout to ensure the aggregator caps word count, removes duplicates, and injects polite notes.

**Acceptance Scenarios**:

1. **Given** both agents succeed, **When** aggregation completes, **Then** the response contains a single ≤60-word paragraph blending both insights plus the exact disclaimer text.
2. **Given** CityAgent fails after retries, **When** WeatherAgent succeeds, **Then** the final response mentions the city guidance degradation, shares the available weather insight, and still includes the disclaimer.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- What happens when Azure OpenAI returns incomplete data for one agent?
- How does the system handle city inputs it cannot resolve or unsafe content in the self introduction?
- How is the experience degraded when streaming fails mid-response?
- What if both agents exceed the timeout simultaneously?
- How do we prevent duplicate or contradictory sentences when aggregating near-identical agent outputs?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST greet the user, collect a one-sentence self introduction and city, and acknowledge limitations before proceeding.
- **FR-002**: System MUST orchestrate WeatherAgent and CityAgent concurrently via ConcurrentBuilder and stream intermediate updates to the client.
- **FR-003**: System MUST generate a single combined tip under ~60 words, append the disclaimer "information is approximate—verify locally before planning," and avoid duplicate details.
- **FR-004**: System MUST degrade gracefully with a polite note if either agent fails while still delivering available insights.
- **FR-005**: System MUST rely solely on Azure OpenAI via Microsoft Foundry with no hardcoded datasets or external weather APIs.
- **FR-006**: System MUST validate that the self introduction is exactly one sentence containing a city name and provide actionable error feedback otherwise.
- **FR-007**: System MUST begin streaming status updates within 2 seconds of submission and tag each update with its originating agent.
- **FR-008**: System MUST emit structured logs that prove concurrent execution, retry outcomes, and final aggregation decisions whenever the local server processes a session.

### Key Entities *(include if feature involves data)*

- **SessionContext**: Tracks the user's introduction, city, streaming state, and error flags without persisting PII.
- **AgentResultEnvelope**: Wraps individual agent outputs, timestamps, and degradation signals for aggregation.
- **StreamEvent**: Represents a single UI-update payload containing agent label, message snippet, timestamp, and severity (info, waiting, degraded).

## Assumptions

- Streaming updates appear as a vertically stacked timeline on the single-page form, avoiding complex frontend frameworks.
- Azure OpenAI configuration (deployment names, region, keys) is available via environment variables and injected at runtime.
- The local development server supports live reloading for demos; production hardening (auth, persistence) is explicitly out of scope per non-goals.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: ≥95% of sessions deliver the combined tip in under 60 words and include the required disclaimer.
- **SC-002**: Streaming of at least one agent update begins within 2 seconds of both inputs being submitted.
- **SC-003**: Degradation notice is emitted for 100% of agent failures while still returning available insights.
- **SC-004**: Telemetry confirms 0 calls per session to non-Azure OpenAI data sources or static lookup tables.
