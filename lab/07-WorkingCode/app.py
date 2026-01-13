"""FastAPI entrypoint for the HelloWeather prototype.

Run locally with:
	uvicorn app:app --reload

The app renders a simple form that collects a one-sentence introduction and a
separate city field, then streams concurrent WeatherAgent and CityAgent updates
via Server-Sent Events (SSE).
"""

from __future__ import annotations

import json
import logging
import re
from typing import AsyncGenerator, Dict, Iterable

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from agents import aggregate_agent_outputs, stream_weather_and_city_tips


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
LOGGER = logging.getLogger("helloweather.app")

app = FastAPI(title="HelloWeather")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
	"""Render the landing page with the HelloWeather form."""

	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(payload: Dict[str, str] = Body(...)) -> StreamingResponse:
	"""Validate inputs, launch concurrent agents, and stream SSE updates."""

	introduction = (payload.get("introduction") or "").strip()
	city = (payload.get("city") or "").strip()

	errors = _validate_inputs(introduction, city)
	if errors:
		raise HTTPException(status_code=422, detail=errors)

	async def event_stream() -> AsyncGenerator[str, None]:
		try:
			async for event in stream_weather_and_city_tips(introduction=introduction, city=city):
				yield _format_sse(event)
		except Exception as exc:  # pragma: no cover - protects live streaming session
			LOGGER.exception("Streaming failed: %s", exc)
			failure_payload = {
				"event": "degraded",
				"data": "We hit a hiccup contacting the agents. Please retry in a moment.",
			}
			yield _format_sse(failure_payload)
			final_payload = {
				"event": "final",
				"data": aggregate_agent_outputs(
					city,
					{
						"weather": {"status": "failed", "text": ""},
						"city": {"status": "failed", "text": ""},
					},
				),
			}
			yield _format_sse(final_payload)

	return StreamingResponse(event_stream(), media_type="text/event-stream")


def _validate_inputs(introduction: str, city: str) -> Iterable[str]:
	"""Return validation errors for introduction + city fields."""

	errors = []
	if not introduction:
		errors.append("Introduction is required.")
	if len(introduction.split()) > 60:
		errors.append("Introduction should stay under 60 words for clarity.")

	if introduction:
		sentence_endings = re.findall(r"[.!?]", introduction)
		if len(sentence_endings) != 1 or introduction.count("\n") > 0:
			errors.append("Please share exactly one sentence in your introduction.")

	if not city:
		errors.append("City is required.")
	elif city.lower() not in introduction.lower():
		errors.append("Mention the city within your introduction sentence so the agents share context.")

	disallowed_terms = {"diagnosis", "prescription", "lawsuit"}
	if any(term in introduction.lower() for term in disallowed_terms):
		errors.append("Please avoid medical or legal requests; HelloWeather shares casual tips only.")

	return errors


def _format_sse(event: Dict[str, str]) -> str:
	"""Convert a structured event dictionary into SSE wire format."""

	event_name = event.get("event", "update")
	payload = {k: v for k, v in event.items() if k not in {"event"}}
	data = event.get("data")
	if data is not None and len(payload) <= 1:
		payload = data
	json_payload = json.dumps(payload, ensure_ascii=False)
	return f"event: {event_name}\ndata: {json_payload}\n\n"

