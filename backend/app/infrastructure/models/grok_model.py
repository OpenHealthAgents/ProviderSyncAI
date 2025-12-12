"""Grok model adapter using LangChain."""
from typing import Optional, Any
from langchain_openai import ChatOpenAI
from ..settings import settings

def GrokModel(
    api_key: Optional[str] = None,
    model_name: str = "grok-beta",
    temperature: float = 0.7,
    **kwargs: Any,
) -> ChatOpenAI:
    """
    Returns a configured ChatOpenAI instance pointing to xAI's API.
    """
    key = api_key or settings.grok_api_key
    if not key:
        raise ValueError("GROK_API_KEY must be set in environment variables or passed as parameter")
    
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=key,
        base_url="https://api.x.ai/v1",
        **kwargs
    )

