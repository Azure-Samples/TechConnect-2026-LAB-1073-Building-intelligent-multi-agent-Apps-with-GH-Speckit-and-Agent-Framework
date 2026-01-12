# Data Model — HelloWeather Web App

## SessionContext
- **Purpose**: Captures a single user submission lifecycle without persisting sensitive data.
- **Fields**:
  - `submission_id: UUID` — generated per request to correlate logs and stream events.
  - `introduction: str` — validated one-sentence input provided by the user.
  - `city: str` — extracted/lowercased city token used in agent prompts.
  - `start_time: datetime` — timestamp when orchestration begins.
  - `status: Literal["pending","streaming","completed","degraded","failed"]` — high-level lifecycle state.
  - `errors: list[str]` — non-fatal warnings surfaced to the aggregator.
- **Relationships**: Aggregator references SessionContext to append degradation notes; StreamEvents reference `submission_id` for grouping.
- **Validation Rules**:
  - `introduction` must be ≤ 200 characters and contain exactly one sentence terminator.
  - `city` must match the canonicalized city extracted from `introduction`.
  - `errors` remains empty unless an agent timeouts or validation warns the user.

## AgentResultEnvelope
- **Purpose**: Uniform wrapper around WeatherAgent and CityAgent outputs for aggregation and logging.
- **Fields**:
  - `agent_name: Literal["weather","city"]`
  - `message: str` — short natural-language insight produced by the agent.
  - `tokens_used: int` — token count returned by Agent Framework metadata (0 when mocked).
  - `duration_ms: int` — elapsed time for the agent's final response.
  - `status: Literal["success","timeout","error"]`
  - `metadata: dict[str, Any]` — optional structured details (e.g., retry_count, model_version).
- **Relationships**: Aggregator consumes a list of envelopes to build the final tip; Telemetry logs each envelope event.
- **Validation Rules**:
  - `message` must be non-empty on `success`.
  - `status != "success"` requires aggregator to produce a degradation note.
  - `duration_ms` must be ≥ 0 and align with telemetry timers.

## StreamEvent
- **Purpose**: Represents each chunk sent to the browser via SSE.
- **Fields**:
  - `event_id: str` — monotonic identifier (e.g., `weather-1`).
  - `submission_id: UUID`
  - `agent: Literal["system","weather","city","aggregator"]`
  - `event_type: Literal["info","update","heartbeat","degraded","final"]`
  - `payload: str` — content rendered in the browser.
  - `timestamp: datetime`
- **Relationships**: Emitted by the orchestration pipeline; the frontend timeline subscribes and displays events.
- **Validation Rules**:
  - `event_type == "final"` occurs exactly once per submission.
  - Heartbeats must contain non-sensitive payload (e.g., "Still thinking...").
  - `payload` for agent updates must reference the agent by name for transparency.

## AggregatedTip
- **Purpose**: Final combined message delivered to the user.
- **Fields**:
  - `content: str` — concatenated insight ≤ 60 words.
  - `degraded_agents: list[str]` — names of agents that failed.
  - `disclaimer: str` — fixed string "information is approximate—verify locally before planning".
  - `word_count: int` — cached word count for validation.
- **Relationships**: Produced from SessionContext + AgentResultEnvelope collection at completion.
- **Validation Rules**:
  - `word_count` must equal the count derived from `content`.
  - `content` must include at least one clause referencing the city.
  - When `degraded_agents` is non-empty, `content` must include a polite note.

## TelemetryRecord
- **Purpose**: Structured log entry for observability dashboards.
- **Fields**:
  - `submission_id: UUID`
  - `agent: Literal["weather","city","aggregator"]`
  - `event: str` — e.g., `"start"`, `"stream_chunk"`, `"retry"`, `"complete"`.
  - `elapsed_ms: int`
  - `status: Literal["ok","retry","degraded","error"]`
  - `details: dict[str, Any]`
- **Relationships**: Derived from StreamEvents and AgentResultEnvelopes; persisted only in logs (not stored in a database).
- **Validation Rules**:
  - `elapsed_ms` must be monotonic within a submission.
  - `status` transitions follow allowed sequence: `ok` → `retry` → `degraded`/`error`.
