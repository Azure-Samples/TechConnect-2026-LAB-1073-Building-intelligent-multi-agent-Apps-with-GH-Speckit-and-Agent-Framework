<!--
Sync Impact Report
Version change: — → 1.0.0
Modified principles:
- Safety & Tone Assurance
- Truthful Azure-Sourced Guidance
- Respectful Input Transparency
- Microsoft Agent Framework Discipline
- Concurrent Orchestration Fidelity
Added sections:
- Purpose & Experience Contract
- Agent Roles & Delivery Criteria
Removed sections:
- none
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
Follow-up TODOs:
- none
-->

# HelloWeather Constitution

## Core Principles

### Safety & Tone Assurance
HelloWeather interactions MUST remain kind, helpful, and concise while avoiding medical or legal advice. Every final response MUST include the disclaimer "information is approximate—verify locally before planning," and the experience MUST preserve a courteous tone regardless of upstream failures.

### Truthful Azure-Sourced Guidance
WeatherAgent and CityAgent MUST rely solely on live reasoning through the Azure OpenAI endpoint; the system MUST NOT embed hardcoded facts, cached weather tables, or external APIs when producing tips.

### Respectful Input Transparency
The experience MUST collect only a one-sentence self introduction and a city, ask for them once per session, and clearly communicate the approximate nature of its guidance and any limitations before delivering results.

### Microsoft Agent Framework Discipline
All agentic logic MUST be implemented in Python using the Microsoft Agent Framework, with Azure OpenAI models provisioned via Microsoft Foundry; no alternative AI runtimes, SDKs, or unmanaged dependencies are permitted.

### Concurrent Orchestration Fidelity
WeatherAgent and CityAgent MUST run in parallel through ConcurrentBuilder, stream progress updates, and feed a final aggregator that merges results, removes duplication, enforces the <60-word combined tip, and adds a polite note whenever one agent fails.

## Purpose & Experience Contract

- Deliver a friendly HelloWeather greeting that elicits a one-sentence self introduction and the user's city.
- Return exactly one combined tip blending weather and city guidance, appended with the mandatory disclaimer.
- Showcase the multi-agent concurrency pattern so that parallel execution and streaming aggregation are obvious to the end user.

## Agent Roles & Delivery Criteria

- **WeatherAgent**: Produce a 1–2 sentence approximate weather tip for the requested city using Azure OpenAI reasoning only.
- **CityAgent**: Produce one concise sentence of situational city guidance (transit, neighborhood, timing, or safety) using Azure OpenAI reasoning only.
- **Aggregator**: Stream intermediate updates from each agent, consolidate them into a single concise final output, and remove redundant details while flagging degraded agent output with a courteous notice.
- **Success Criteria**: Parallel execution with visible streaming, graceful degradation on agent failure, and a final response under ~60 words that still communicates the greeting, combined insight, and disclaimer.
- **Non-Goals**: Real-time meteorological accuracy, geolocation, and integration with external weather or city data services.

## Governance

This constitution is the authoritative contract for HelloWeather delivery. Every plan, spec, task list, and code review MUST demonstrate compliance, explicitly confirming the disclaimer, concurrency pattern, dependency boundaries, and non-use of hardcoded data. Amendments require consensus from project maintainers, an impact assessment on active work, and synchronized template updates. Versioning follows semantic rules (MAJOR for breaking governance or principle removals, MINOR for new principles or sections, PATCH for clarifications). Compliance reviews occur before merging any change to ensure principles remain verifiable in tests and runtime instrumentation.

**Version**: 1.0.0 | **Ratified**: 2026-01-10 | **Last Amended**: 2026-01-10
