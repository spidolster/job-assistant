"""
config.py — Manage persistent configuration (API keys, provider settings).
Reads and writes to the local .env file so settings survive restarts.
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

# Path to the .env file (project root)
_ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
_config_loaded = False

def _ensure_env_file():
    """Create .env if it doesn't exist."""
    if not _ENV_PATH.exists():
        _ENV_PATH.touch()

def load_config(force: bool = False):
    """Load .env into environment variables. Skips if already loaded unless force=True."""
    global _config_loaded
    if _config_loaded and not force:
        return
    _ensure_env_file()
    load_dotenv(_ENV_PATH, override=True)
    _config_loaded = True

def save_api_key(provider: str, key: str):
    """
    Save an API key to the .env file for the given provider.
    Args:
        provider: 'openai' or 'deepseek'
        key: The API key string.
    """
    _ensure_env_file()
    env_var = f"{provider.upper()}_API_KEY"
    set_key(str(_ENV_PATH), env_var, key)
    os.environ[env_var] = key

def get_api_key(provider: str) -> str:
    """
    Get the saved API key for a provider.
    Args:
        provider: 'openai' or 'deepseek'
    Returns:
        The API key string, or empty string if not set.
    """
    load_config()  # Uses cached read unless force=True
    env_var = f"{provider.upper()}_API_KEY"
    value = os.getenv(env_var, "")
    # Don't return placeholder values
    if value.startswith("your_"):
        return ""
    return value

def save_provider(provider: str):
    """Save the selected AI provider to .env."""
    _ensure_env_file()
    set_key(str(_ENV_PATH), "AI_PROVIDER", provider.lower())
    os.environ["AI_PROVIDER"] = provider.lower()

def get_provider() -> str:
    """Get the saved AI provider."""
    load_config()
    return os.getenv("AI_PROVIDER", "openai")

def save_model(model_name: str):
    """Save the selected model name to .env."""
    _ensure_env_file()
    set_key(str(_ENV_PATH), "AI_MODEL", model_name)
    os.environ["AI_MODEL"] = model_name

def get_model() -> str:
    """Get the saved model name."""
    load_config()
    return os.getenv("AI_MODEL", "")

def get_gemini_extract_key() -> str:
    """Get the dedicated Gemini API key for JD auto-extraction.

    Reads GEMINI_EXTRACT_API_KEY from .env.
    Falls back to GEMINI_API_KEY if the dedicated key is not set.
    """
    load_config()
    key = os.getenv("GEMINI_EXTRACT_API_KEY", "")
    if not key:
        key = os.getenv("GEMINI_API_KEY", "")
    return key

# Available models per provider
AVAILABLE_MODELS = {
    "openai": [
        "gpt-4.1-nano",
        "gpt-4.1-mini",
        "gpt-4.1",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ],
    "deepseek": [
        "deepseek-chat",
        "deepseek-coder",
        "deepseek-reasoner",
    ],
    "gemini": [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ],
    "claude": [
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-haiku-20241022",
    ],
}
