from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

from data.mock_data import get_default_places
from utils.config import get_openai_api_key, get_openai_model

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - fallback for missing dependency
    OpenAI = None


def _coerce_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value).date()
    return date.today()


def _trip_day_count(trip_input: dict[str, Any]) -> int:
    start = _coerce_date(trip_input.get("start_date"))
    end = _coerce_date(trip_input.get("end_date"))
    delta = (end - start).days + 1
    return max(1, delta)


def _build_mock_itinerary(trip_input: dict[str, Any]) -> dict[str, Any]:
    destination = str(trip_input.get("destination", "your destination")).strip() or "your destination"
    days = _trip_day_count(trip_input)
    travelers = int(trip_input.get("traveler_count", 1) or 1)
    budget_range = trip_input.get("budget_range", "Not specified")
    preferences = trip_input.get("preferences", [])

    places = get_default_places(destination)
    daily_plan: list[dict[str, Any]] = []

    for day in range(1, days + 1):
        morning_place = places[(day - 1) % len(places)]
        afternoon_place = places[day % len(places)]
        evening_place = places[(day + 1) % len(places)]
        preference_note = (
            f"Prioritize {', '.join(preferences[:2])} experiences."
            if preferences
            else "Keep activities balanced between sightseeing and rest."
        )

        daily_plan.append(
            {
                "day": day,
                "title": f"Day {day} in {destination.title()}",
                "morning": f"Visit {morning_place} and enjoy a guided walk.",
                "afternoon": f"Explore {afternoon_place} with local food nearby.",
                "evening": f"Wind down around {evening_place} and local nightlife.",
                "places": [morning_place, afternoon_place, evening_place],
                "note": preference_note,
            }
        )

    budget_multiplier = {"Budget": 110, "Mid-range": 200, "Luxury": 380}.get(budget_range, 170)
    estimated_total_cost = float(days * travelers * budget_multiplier)

    return {
        "destination": destination.title(),
        "overview": f"{days}-day itinerary for {destination.title()} tailored for {travelers} traveler(s).",
        "daily_plan": daily_plan,
        "estimated_total_cost": round(estimated_total_cost, 2),
        "currency": "USD",
        "source": "mock_fallback",
    }


def _get_openai_client() -> Any | None:
    api_key = get_openai_api_key()
    if not api_key or OpenAI is None:
        return None
    return OpenAI(api_key=api_key)


def _request_json(messages: list[dict[str, str]]) -> dict[str, Any] | None:
    client = _get_openai_client()
    if client is None:
        return None

    try:
        response = client.chat.completions.create(
            model=get_openai_model(),
            messages=messages,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        return None
    return None


def _sanitize_itinerary(raw: dict[str, Any], trip_input: dict[str, Any]) -> dict[str, Any]:
    if not raw:
        return _build_mock_itinerary(trip_input)

    destination = str(raw.get("destination") or trip_input.get("destination") or "Unknown").strip().title()
    overview = str(raw.get("overview") or f"Itinerary for {destination}.").strip()

    daily_plan_raw = raw.get("daily_plan", [])
    if not isinstance(daily_plan_raw, list) or not daily_plan_raw:
        return _build_mock_itinerary(trip_input)

    normalized_daily_plan: list[dict[str, Any]] = []
    for idx, item in enumerate(daily_plan_raw, start=1):
        if not isinstance(item, dict):
            continue

        places = item.get("places", [])
        if not isinstance(places, list):
            places = []

        normalized_daily_plan.append(
            {
                "day": int(item.get("day", idx) or idx),
                "title": str(item.get("title") or f"Day {idx} in {destination}"),
                "morning": str(item.get("morning") or "Morning free exploration."),
                "afternoon": str(item.get("afternoon") or "Afternoon city exploration."),
                "evening": str(item.get("evening") or "Evening relaxation and local dining."),
                "places": [str(place).strip() for place in places if str(place).strip()],
                "note": str(item.get("note") or ""),
            }
        )

    if not normalized_daily_plan:
        return _build_mock_itinerary(trip_input)

    estimated_total_cost = raw.get("estimated_total_cost")
    try:
        estimated_total_cost = float(estimated_total_cost)
    except (TypeError, ValueError):
        estimated_total_cost = _build_mock_itinerary(trip_input)["estimated_total_cost"]

    return {
        "destination": destination,
        "overview": overview,
        "daily_plan": normalized_daily_plan,
        "estimated_total_cost": round(estimated_total_cost, 2),
        "currency": str(raw.get("currency") or "USD"),
        "source": str(raw.get("source") or "openai"),
    }


def generate_itinerary(trip_input: dict[str, Any]) -> dict[str, Any]:
    prompt = {
        "destination": trip_input.get("destination"),
        "start_date": str(trip_input.get("start_date")),
        "end_date": str(trip_input.get("end_date")),
        "traveler_count": trip_input.get("traveler_count", 1),
        "budget_range": trip_input.get("budget_range"),
        "preferences": trip_input.get("preferences", []),
    }

    messages = [
        {
            "role": "system",
            "content": (
                "You are a travel planner. Return valid JSON only with keys: "
                "destination, overview, daily_plan, estimated_total_cost, currency, source. "
                "daily_plan must be a list of day objects with keys: day, title, morning, afternoon, evening, places, note."
            ),
        },
        {
            "role": "user",
            "content": f"Create an itinerary using this input: {json.dumps(prompt)}",
        },
    ]

    raw = _request_json(messages)
    return _sanitize_itinerary(raw or {}, trip_input)


def edit_itinerary(
    current_itinerary: dict[str, Any],
    edit_request: str,
    trip_input: dict[str, Any],
) -> dict[str, Any]:
    if not current_itinerary:
        return generate_itinerary(trip_input)
    if not edit_request.strip():
        return current_itinerary

    messages = [
        {
            "role": "system",
            "content": (
                "You update travel itineraries. Preserve valid structure and return JSON only with keys: "
                "destination, overview, daily_plan, estimated_total_cost, currency, source."
            ),
        },
        {
            "role": "user",
            "content": (
                "Update the itinerary according to this user request while preserving context.\n"
                f"Request: {edit_request}\n"
                f"Current itinerary: {json.dumps(current_itinerary)}"
            ),
        },
    ]

    raw = _request_json(messages)
    if raw:
        return _sanitize_itinerary(raw, trip_input)

    fallback = _sanitize_itinerary(current_itinerary, trip_input)
    fallback["overview"] = f"{fallback['overview']} Updated request: {edit_request.strip()}"
    fallback["source"] = "mock_fallback"
    if fallback["daily_plan"]:
        fallback["daily_plan"][0]["note"] = (
            f"Adjustment requested by user: {edit_request.strip()}"
        )
    return fallback


def _fallback_chat_reply(message: str, itinerary: dict[str, Any], trip_input: dict[str, Any]) -> str:
    user_text = message.lower()
    destination = str(trip_input.get("destination") or itinerary.get("destination") or "this destination")

    if "budget" in user_text:
        return "For better budget control, book transport early, stay near public transit, and prioritize free attractions in the morning."
    if "food" in user_text:
        return f"In {destination.title()}, mix one local market meal with one popular restaurant each day to balance cost and experience."
    if "itinerary" in user_text and itinerary.get("daily_plan"):
        first_day = itinerary["daily_plan"][0]
        return f"Your itinerary starts with: {first_day.get('morning', 'a city walk')}."
    return f"For {destination.title()}, keep travel buffers between activities and reserve at least one flexible evening."


def chatbot_reply(
    message: str,
    itinerary: dict[str, Any],
    trip_input: dict[str, Any],
    chat_history: list[dict[str, str]],
) -> str:
    client = _get_openai_client()
    if client is None:
        return _fallback_chat_reply(message, itinerary, trip_input)

    itinerary_context = json.dumps(itinerary) if itinerary else "No itinerary yet"
    trip_context = json.dumps(
        {
            "destination": trip_input.get("destination"),
            "dates": [str(trip_input.get("start_date")), str(trip_input.get("end_date"))],
            "budget": trip_input.get("budget_range"),
            "preferences": trip_input.get("preferences", []),
        }
    )

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are an AI travel assistant. Keep responses concise and practical. "
                "Use current trip context when relevant."
            ),
        },
        {
            "role": "system",
            "content": f"Trip context: {trip_context}. Itinerary context: {itinerary_context}",
        },
    ]

    for item in chat_history[-6:]:
        role = item.get("role", "assistant")
        content = item.get("content", "")
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=get_openai_model(),
            messages=messages,
            temperature=0.4,
        )
        content = response.choices[0].message.content
        if content:
            return content.strip()
    except Exception:
        return _fallback_chat_reply(message, itinerary, trip_input)

    return _fallback_chat_reply(message, itinerary, trip_input)


def generate_transport_options(source_location: str, destination: str, traveler_count: int = 1) -> list[dict[str, Any]] | None:
    """Use LLM to generate realistic transport options from source to destination."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a travel data API. Return valid JSON only with a key 'options' containing a list of "
                "3-4 transport options from the source city to the destination city. Each option must have keys: "
                "id (string like TR-XXX-001), destination (lowercase destination city), type (Flight/Train/Bus), "
                "provider (realistic airline/train/bus company that operates between these cities), "
                "price (float, realistic USD price for this route), departure_time (HH:MM), arrival_time (HH:MM), "
                "duration (string like '6h 35m'). Use realistic providers and prices for this specific route."
            ),
        },
        {
            "role": "user",
            "content": f"Generate transport options from {source_location} to {destination}.",
        },
    ]
    raw = _request_json(messages)
    if raw and isinstance(raw.get("options"), list):
        options = []
        for item in raw["options"]:
            if not isinstance(item, dict):
                continue
            try:
                opt = {
                    "id": str(item.get("id", f"TR-AI-{len(options)+1:03d}")),
                    "destination": str(item.get("destination", destination)).strip().lower(),
                    "type": str(item.get("type", "Flight")),
                    "provider": str(item.get("provider", "Unknown")),
                    "price": float(item.get("price", 0)),
                    "departure_time": str(item.get("departure_time", "00:00")),
                    "arrival_time": str(item.get("arrival_time", "00:00")),
                    "duration": str(item.get("duration", "N/A")),
                }
                opt["price_per_traveler"] = opt["price"]
                opt["total_price"] = round(opt["price"] * traveler_count, 2)
                options.append(opt)
            except (TypeError, ValueError):
                continue
        if options:
            return options
    return None


def generate_local_transport(destination: str) -> list[dict[str, Any]] | None:
    """Use LLM to generate local transport options at the destination."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a travel data API. Return valid JSON only with a key 'local_transport' containing a list of "
                "4-5 local transport options available within the given city. Each option must have keys: "
                "id (string like LT-XXX-001), type (Metro/Bus/Taxi/Rickshaw/Tram/Ferry/Ride-share etc.), "
                "name (specific service name like 'Dubai Metro Red Line', 'Tokyo JR Pass'), "
                "price_range (string like '$2-5 per ride'), "
                "description (1 sentence about coverage/usefulness for tourists), "
                "recommended (boolean, true if best for tourists). "
                "Use real local transport systems for the given city."
            ),
        },
        {
            "role": "user",
            "content": f"Generate local transport options available in {destination} for tourists.",
        },
    ]
    raw = _request_json(messages)
    if raw and isinstance(raw.get("local_transport"), list):
        local = []
        for item in raw["local_transport"]:
            if not isinstance(item, dict):
                continue
            try:
                lt = {
                    "id": str(item.get("id", f"LT-AI-{len(local)+1:03d}")),
                    "type": str(item.get("type", "Bus")),
                    "name": str(item.get("name", "Local Transport")),
                    "price_range": str(item.get("price_range", "Varies")),
                    "description": str(item.get("description", "")),
                    "recommended": bool(item.get("recommended", False)),
                }
                local.append(lt)
            except (TypeError, ValueError):
                continue
        if local:
            return local
    return None


def generate_hotel_options(destination: str, budget_range: str = "Not specified") -> list[dict[str, Any]] | None:
    """Use LLM to generate realistic hotel options for any destination."""
    budget_hint = f" The user's budget preference is: {budget_range}." if budget_range != "Not specified" else ""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a travel data API. Return valid JSON only with a key 'hotels' containing a list of "
                "3-4 hotel options for the given destination. Each hotel must have keys: "
                "id (string like HT-XXX-001), destination (lowercase city name), name (realistic hotel name), "
                "price_per_night (float, realistic USD price), rating (float 3.5-5.0), "
                "location (specific area/neighborhood), amenities (list of 2-4 strings), "
                "image_url (use a relevant Unsplash image URL like https://images.unsplash.com/photo-XXXX). "
                "Use realistic hotel names, prices, and locations for the given destination." + budget_hint
            ),
        },
        {
            "role": "user",
            "content": f"Generate hotel options for {destination}.",
        },
    ]
    raw = _request_json(messages)
    if raw and isinstance(raw.get("hotels"), list):
        hotels = []
        for item in raw["hotels"]:
            if not isinstance(item, dict):
                continue
            try:
                hotel = {
                    "id": str(item.get("id", f"HT-AI-{len(hotels)+1:03d}")),
                    "destination": str(item.get("destination", destination)).strip().lower(),
                    "name": str(item.get("name", "Hotel")),
                    "price_per_night": float(item.get("price_per_night", 100)),
                    "rating": min(5.0, max(1.0, float(item.get("rating", 4.0)))),
                    "location": str(item.get("location", destination)),
                    "amenities": list(item.get("amenities", ["WiFi"])),
                    "image_url": str(item.get("image_url", "https://images.unsplash.com/photo-1455587734955-081b22074882")),
                }
                hotels.append(hotel)
            except (TypeError, ValueError):
                continue
        if hotels:
            return hotels
    return None

