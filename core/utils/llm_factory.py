import os
from typing import Any
from dotenv import load_dotenv

## LLM Provider Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# === Utility to resolve env vars ===
def resolve_env_var(value: str) -> str:
    if isinstance(value, str) and value.startswith("env:"):
        env_var = value.split("env:")[1]
        return os.getenv(env_var)
    return value

# === LLM Provider Factory ===
def get_llm(llm_config: dict) -> Any:
    """
    Initializes and returns an LLM instance based on the provided configuration.
    This function is designed to be called by individual components (e.g., AgentComponent),
    allowing each component to have its own LLM configuration.
    """
    if not llm_config or not llm_config.get("model"):
        return None

    model_name = llm_config.get("model", "")
    provider = llm_config.get("provider", "").lower()

    # --- Infer provider from model name if not explicitly set ---
    if not provider:
        if "gemini" in model_name:
            provider = "googlegenerativeai"
        elif "gpt" in model_name:
            provider = "openai"
        elif "deepseek" in model_name:
            provider = "deepseek"
        else:
            provider = "googlegenerativeai"  # Default fallback

    # --- Get API Key from environment variables ---
    api_key_env_map = {
        "googlegenerativeai": "GOOGLE_API_KEY",
        "openai": "OPENAI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
    }
    api_key_env_var = api_key_env_map.get(provider)
    api_key = os.getenv(api_key_env_var) if api_key_env_var else None
    
    # Allow overriding from config for flexibility
    if llm_config.get("api_key"):
        api_key = resolve_env_var(llm_config.get("api_key"))

    # --- Get model-specific parameters ---
    params = {"model": model_name, "api_key": api_key}
    if "temperature" in llm_config and llm_config["temperature"] is not None:
        params["temperature"] = llm_config["temperature"]
    if "max_tokens" in llm_config and llm_config["max_tokens"] is not None:
        params["max_tokens"] = llm_config["max_tokens"]

    # --- Instantiate and return the correct LLM client ---
    try:
        if provider == "googlegenerativeai":
            params.pop("max_tokens", None)  # Not supported by this provider
            params["google_api_key"] = params.pop("api_key", None)
            return ChatGoogleGenerativeAI(**params)
        elif provider == "openai":
            return ChatOpenAI(**params)
        elif provider == "deepseek":
            return ChatDeepSeek(**params)
        else:
            return None
    except Exception as e:
        # Handle potential initialization errors, e.g., missing API keys
        print(f"Error initializing LLM provider '{provider}': {e}")
        return None 