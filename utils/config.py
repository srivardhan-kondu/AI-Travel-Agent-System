import os


def get_openai_api_key() -> str:
    """Return OpenAI API key from environment, or an empty string if unset."""
    return os.getenv("OPENAI_API_KEY", "").strip()


def get_openai_model() -> str:
    """Return configured OpenAI model used for itinerary and chat features."""
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
