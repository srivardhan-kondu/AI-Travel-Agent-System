from __future__ import annotations

from typing import Any

from data.mock_data import get_hotel_data, normalize_destination, HOTEL_DATA
from services.ai_service import generate_transport_options, generate_hotel_options, generate_local_transport


def _filter_hotels_by_budget(hotels: list[dict[str, Any]], budget_range: str) -> list[dict[str, Any]]:
    if budget_range == "Budget":
        return [hotel for hotel in hotels if hotel["price_per_night"] <= 120]
    if budget_range == "Mid-range":
        return [hotel for hotel in hotels if 120 < hotel["price_per_night"] <= 240]
    if budget_range == "Luxury":
        return [hotel for hotel in hotels if hotel["price_per_night"] > 240]
    return hotels


def fetch_transport_options(trip_input: dict[str, Any]) -> list[dict[str, Any]]:
    """Fetch transport options using LLM (source → destination)."""
    source_location = trip_input.get("source_location", "")
    destination = trip_input.get("destination", "")
    traveler_count = max(1, int(trip_input.get("traveler_count", 1) or 1))

    ai_options = generate_transport_options(source_location, destination, traveler_count)
    if ai_options:
        return ai_options

    # Fallback: generate a minimal placeholder
    return [
        {
            "id": "TR-FB-001",
            "destination": destination.strip().lower(),
            "type": "Flight",
            "provider": "Standard Airlines",
            "price": 500.0,
            "departure_time": "08:00",
            "arrival_time": "14:00",
            "duration": "6h 00m",
            "price_per_traveler": 500.0,
            "total_price": round(500.0 * traveler_count, 2),
        }
    ]


def fetch_local_transport(trip_input: dict[str, Any]) -> list[dict[str, Any]]:
    """Fetch local transport options at the destination using LLM."""
    destination = trip_input.get("destination", "")
    local = generate_local_transport(destination)
    if local:
        return local
    return [
        {"id": "LT-FB-001", "type": "Taxi", "name": "Local Taxi", "price_range": "Varies", "description": "Available throughout the city.", "recommended": True},
    ]


def fetch_hotel_options(trip_input: dict[str, Any]) -> list[dict[str, Any]]:
    """Fetch hotel options — uses static data for known destinations, LLM for others."""
    destination = trip_input.get("destination", "")
    budget_range = trip_input.get("budget_range", "Not specified")
    normalized = normalize_destination(destination)

    # Check if we have static data
    static = get_hotel_data(destination)
    if static and any(h["destination"] == normalized for h in static):
        filtered = _filter_hotels_by_budget(static, budget_range)
        return filtered or static

    # Use LLM for unknown destinations
    ai_hotels = generate_hotel_options(destination, budget_range)
    if ai_hotels:
        return ai_hotels

    # Final fallback
    from copy import deepcopy
    options = deepcopy(HOTEL_DATA[:3])
    for option in options:
        option["destination"] = normalized
    filtered = _filter_hotels_by_budget(options, budget_range)
    return filtered or options
