# Research Summary — HelloWeather Web App

## Mocking Agent Framework Streaming in Tests
- **Decision**: Use Microsoft Agent Framework's `MockLLM` with scripted responses plus a stub streaming transport fixture to exercise the ConcurrentBuilder async generator under pytest-asyncio.
- **Rationale**: `MockLLM` keeps tests deterministic, avoids Azure usage, and the stub transport lets us capture event payloads for assertions on sequencing and degradation notes without relying on real timing.
- **Alternatives considered**: 
  - Capturing live Azure OpenAI streams (rejected: slow, flaky, violates no-static-data intent). 
  - Monkeypatching agent `run` methods to return static strings (rejected: bypasses streaming behavior and concurrency validation).

## HTTP Streaming Strategy
- **Decision**: Expose incremental updates to the browser via Server-Sent Events (SSE) implemented through FastAPI's `EventSourceResponse` helper.
- **Rationale**: SSE pairs well with one-way status updates, integrates with FastAPI, and keeps the frontend simple while preserving streaming semantics required by the constitution.
- **Alternatives considered**: 
  - Raw chunked responses (harder to consume in plain JS, more boilerplate). 
  - WebSockets (overkill for one-way streaming; adds complexity for workshop audience).

## Aggregation Deduplication Approach
- **Decision**: Normalize agent sentences (lowercase, strip punctuation) and keep a set to avoid duplicate guidance before composing the final paragraph.
- **Rationale**: Ensures merged content stays under 60 words and avoids redundant information when both agents produce similar phrasing.
- **Alternatives considered**: 
  - Heavier semantic similarity checks (rejected: unnecessary complexity). 
  - Blind concatenation (rejected: risks duplicated or contradictory messaging).
