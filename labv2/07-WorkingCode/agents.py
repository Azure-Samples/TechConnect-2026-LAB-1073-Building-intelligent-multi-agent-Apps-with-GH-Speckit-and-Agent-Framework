"""HelloWeather agent orchestration helpers.

This module initialises Azure OpenAI chat access, defines WeatherAgent and CityAgent
roles, and exposes utilities that run both agents concurrently while streaming
progress updates suitable for Server-Sent Events (SSE).
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, Iterable, List, Optional, Set

from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv

try:  # Prefer Microsoft Agent Framework when available.
    from agentframework.azure import AzureOpenAIChatClient
    from agentframework.workflows.concurrent import ConcurrentBuilder

    HAVE_AGENT_FRAMEWORK = True
except ImportError:  # pragma: no cover - runtime fallback when dependency is absent
    AzureOpenAIChatClient = Any  # type: ignore[misc, assignment]
    HAVE_AGENT_FRAMEWORK = False

    class ConcurrentBuilder:  # type: ignore[no-redef]
        """Minimal shim so calling code can continue without the real library."""

        def __init__(self) -> None:
            self._participants: List[Dict[str, Any]] = []

        def with_participant(self, name: str, handler: Any) -> "ConcurrentBuilder":
            self._participants.append({"name": name, "handler": handler})
            return self

        def build(self) -> "_SimpleConcurrentWorkflow":
            return _SimpleConcurrentWorkflow(self._participants)


LOGGER = logging.getLogger("helloweather.agents")
DISCLAIMER = "Information is approximate—verify locally before planning."
STREAM_TIMEOUT_SECONDS = 12
RETRY_LIMIT = 1


@dataclass
class AzureSettings:
    """Azure OpenAI configuration parsed from environment variables."""

    endpoint: str
    deployment: str
    api_version: str
    api_key: Optional[str]


def _load_settings() -> AzureSettings:
    """Load Azure OpenAI settings from .env with validation."""

    load_dotenv()
    endpoint = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()
    deployment = (os.getenv("AZURE_OPENAI_DEPLOYMENT") or "").strip()
    if not endpoint or not deployment:
        raise RuntimeError(
            "AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT must be configured via .env"
        )

    api_version = (os.getenv("AZURE_OPENAI_API_VERSION") or "2024-05-01-preview").strip()
    api_key = (os.getenv("AZURE_OPENAI_API_KEY") or None)
    return AzureSettings(endpoint=endpoint, deployment=deployment, api_version=api_version, api_key=api_key)


def create_chat_client() -> AzureOpenAIChatClient:
    """Initialise Azure OpenAI chat client using CLI auth with API key fallback."""

    if not HAVE_AGENT_FRAMEWORK:
        raise RuntimeError(
            "Microsoft Agent Framework is not installed. Install 'agent-framework --pre' to enable live agents."
        )

    settings = _load_settings()

    credential: Optional[Any] = None
    client_kwargs: Dict[str, Any] = {
        "endpoint": settings.endpoint,
        "default_deployment": settings.deployment,
        "api_version": settings.api_version,
    }

    if settings.api_key:
        client_kwargs["api_key"] = settings.api_key
    else:
        try:
            credential = AzureCliCredential()
            credential.get_token("https://management.azure.com/.default")
        except Exception as exc:  # pragma: no cover - environment dependent
            LOGGER.info("Azure CLI credential unavailable: %s", exc)
            credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

        client_kwargs["credential"] = credential

    try:
        return AzureOpenAIChatClient(**client_kwargs)
    except TypeError as exc:  # pragma: no cover - signature drift guardrail
        raise RuntimeError(
            "AzureOpenAIChatClient signature may have changed. Update create_chat_client accordingly."
        ) from exc


class WeatherAgent:
    """Agent that produces a short, approximate weather tip."""

    SYSTEM_PROMPT = (
        "You are WeatherAgent. Given a friendly introduction and city name, "
        "respond with a concise, good-natured weather suggestion. Keep to one or "
        "two sentences, avoid deterministic claims, and remind users conditions can change."
    )

    def __init__(self, client: Optional[Any]) -> None:
        self._client = client

    async def run(self, introduction: str, city: str) -> str:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"The user said: '{introduction}'. Provide a brief, friendly weather tip for {city}. "
                    "Stay approximate and suggest flexible preparation."
                ),
            },
        ]

        if not HAVE_AGENT_FRAMEWORK or not self._client:
            await asyncio.sleep(0.1)
            return f"Skies around {city} can shift quickly, so pack a light layer and stay flexible."

        text = await _invoke_chat(self._client, messages)
        if not text:
            return f"Keep an eye on local updates in {city}; weather can change fast."
        return text


class CityAgent:
    """Agent that produces a short guidance sentence for the requested city."""

    SYSTEM_PROMPT = (
        "You are CityAgent. Offer a single helpful sentence for visitors in the "
        "given city. Mention practical local tips (transit, attire, timing) and avoid claims of certainty."
    )

    def __init__(self, client: Optional[Any]) -> None:
        self._client = client

    async def run(self, introduction: str, city: str) -> str:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"The user introduction was '{introduction}'. Share one short, practical tip for spending time in {city}."
                ),
            },
        ]

        if not HAVE_AGENT_FRAMEWORK or not self._client:
            await asyncio.sleep(0.1)
            return f"Budget a little extra time when moving around {city}; local conditions can vary."

        text = await _invoke_chat(self._client, messages)
        if not text:
            return f"Consider reviewing community forums for current tips about {city}."
        return text


async def stream_weather_and_city_tips(introduction: str, city: str) -> AsyncGenerator[Dict[str, Any], None]:
    """Run WeatherAgent and CityAgent concurrently and stream structured events."""

    yield {
        "event": "info",
        "data": f"Thanks for sharing! Checking fresh guidance for {city} with both agents…",
    }

    client: Optional[Any] = None
    if HAVE_AGENT_FRAMEWORK:
        try:
            client = create_chat_client()
        except Exception as exc:  # pragma: no cover - surfaces during local dev without credentials
            LOGGER.warning("Falling back to mock responses: %s", exc)

    weather_agent = WeatherAgent(client)
    city_agent = CityAgent(client)

    start_time = time.perf_counter()

    async def invoke_agent(name: str, handler: Any) -> Dict[str, Any]:
        agent_start = time.perf_counter()
        last_exc: Optional[Exception] = None
        text = ""
        status = "failed"

        for attempt in range(RETRY_LIMIT + 1):
            try:
                text = await asyncio.wait_for(
                    handler(introduction=introduction, city=city), STREAM_TIMEOUT_SECONDS
                )
                status = "success" if text else "degraded"
                break
            except Exception as exc:  # pragma: no cover - networking/library failures
                last_exc = exc
                status = "failed"
                LOGGER.warning("%sAgent attempt %s failed: %s", name.title(), attempt + 1, exc)
                if attempt < RETRY_LIMIT:
                    await asyncio.sleep(0.2)
                else:
                    text = ""

        duration_ms = int((time.perf_counter() - agent_start) * 1000)
        if status == "failed" and last_exc is not None:
            LOGGER.error("%sAgent failed after retries: %s", name.title(), last_exc)

        return {"status": status, "text": text, "duration_ms": duration_ms}

    tasks: Dict[str, asyncio.Task[Dict[str, Any]]] = {
        "weather": asyncio.create_task(invoke_agent("weather", weather_agent.run)),
        "city": asyncio.create_task(invoke_agent("city", city_agent.run)),
    }

    for agent_name in tasks:
        yield {"event": "update", "agent": agent_name, "data": "Gathering insights…"}

    agent_results: Dict[str, Dict[str, Any]] = {}

    for agent_name, task in tasks.items():
        try:
            result = await task
        except Exception as exc:  # pragma: no cover - protects unexpected task cancellation
            LOGGER.exception("%sAgent task crashed: %s", agent_name.title(), exc)
            result = {"status": "failed", "text": "", "duration_ms": STREAM_TIMEOUT_SECONDS * 1000}

        agent_results[agent_name] = result

        event_type = "update" if result.get("status") == "success" else "degraded"
        message = result.get("text") or f"{agent_name.title()}Agent ran into an issue; no fresh details."
        yield {"event": event_type, "agent": agent_name, "data": message}

    combined = aggregate_agent_outputs(city, agent_results)
    elapsed_ms = int((time.perf_counter() - start_time) * 1000)
    LOGGER.info("Aggregated final tip in %sms", elapsed_ms)

    yield {"event": "final", "data": combined}


def aggregate_agent_outputs(city: str, agent_results: Dict[str, Dict[str, Any]]) -> str:
    """Merge agent messages into a single polite paragraph with deduplication."""

    snippets: List[str] = []
    seen: Set[str] = set()
    degraded: List[str] = []

    for name, envelope in agent_results.items():
        status = (envelope.get("status") or "").lower()
        text = (envelope.get("text") or "").strip()

        if status == "success" and text:
            normalized = _normalize_for_dedup(text)
            if normalized not in seen:
                seen.add(normalized)
                if not text.endswith("."):
                    text = f"{text}."
                snippets.append(text)
        else:
            degraded.append(name)

    if snippets:
        paragraph = " ".join(snippets)
    else:
        paragraph = f"We could not gather fresh insights for {city}."

    if degraded:
        agent_labels = ", ".join(f"{name.title()}Agent" for name in degraded)
        paragraph = f"{paragraph} {agent_labels} encountered delays so treat this as partial guidance."

    if city and city.lower() not in paragraph.lower():
        paragraph = f"In {city}, {paragraph}"

    words = paragraph.split()
    if len(words) > 60:
        paragraph = " ".join(words[:59]) + "…"

    return f"{paragraph.strip()} {DISCLAIMER}".strip()


async def _invoke_chat(client: Any, messages: List[Dict[str, str]]) -> str:
    """Call the Agent Framework client while tolerating signature drift."""

    async def attempt(method_name: str, payload: Dict[str, Any]) -> Optional[str]:
        method = getattr(client, method_name, None)
        if not callable(method):
            return None
        try:
            result = method(**payload)
        except TypeError:
            return None
        if asyncio.iscoroutine(result):
            result = await result
        text = _extract_text(result)
        return text or None

    for method_name in ("complete_chat", "complete", "chat"):
        for payload in ({"messages": messages, "temperature": 0.4}, {"messages": messages}):
            try:
                text = await attempt(method_name, payload)
            except Exception as exc:  # pragma: no cover - surfaces when SDK behaviour changes
                LOGGER.warning("Calling %s on AzureOpenAIChatClient failed: %s", method_name, exc)
                continue
            if text:
                return text

    LOGGER.warning("Azure chat invocation produced no text; using fallback guidance instead.")
    return ""


def _extract_text(response: Any) -> str:
    """Extract model text from Azure OpenAI chat response regardless of SDK shape."""

    content = getattr(response, "content", None)
    if isinstance(content, list) and content:
        pieces = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str) and text.strip():
                pieces.append(text.strip())
        if pieces:
            return " ".join(pieces).strip()

    message = getattr(response, "message", None)
    if isinstance(message, str) and message.strip():
        return message.strip()

    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    return str(response).strip()


def _normalize_for_dedup(text: str) -> str:
    """Lowercase and collapse whitespace so similar snippets deduplicate."""

    return " ".join(text.lower().split())


class _SimpleConcurrentWorkflow:
    """Fallback workflow used when the official ConcurrentBuilder is unavailable."""

    def __init__(self, participants: Iterable[Dict[str, Any]]) -> None:
        self.participants = list(participants)
        self._names = [entry["name"] for entry in self.participants]
        self._handlers = [entry["handler"] for entry in self.participants]

    def with_participant(self, name: str, handler: Any) -> "_SimpleConcurrentWorkflow":
        self.participants.append({"name": name, "handler": handler})
        self._names.append(name)
        self._handlers.append(handler)
        return self

    def build(self) -> "_SimpleConcurrentWorkflow":
        return self

    async def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        tasks = [asyncio.create_task(handler(*args, **kwargs)) for handler in self._handlers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return dict(zip(self._names, results))

