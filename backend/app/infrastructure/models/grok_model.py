"""Grok model adapter for Smolagents."""
from typing import Any, Optional
from smolagents import Model
from smolagents.models import ChatMessage
from xai_sdk import Client
from ..settings import settings


class GrokModel(Model):
    """Grok model wrapper for Smolagents."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "grok-beta",
        temperature: float = 0.7,
        **kwargs: Any,
    ):
        # Initialize base Model with proper parameters
        super().__init__(model_id=model_name, **kwargs)
        self.api_key = api_key or settings.grok_api_key
        if not self.api_key:
            raise ValueError("GROK_API_KEY must be set in environment variables or passed as parameter")
        self.client = Client(api_key=self.api_key)
        self.model_name = model_name
        self.temperature = temperature
    
    async def generate(
        self,
        messages: list[ChatMessage],
        stop_sequences: Optional[list[str]] = None,
        response_format: Optional[dict[str, str]] = None,
        tools_to_call_from: Optional[list] = None,
        **kwargs: Any,
    ) -> ChatMessage:
        """Generate completion using Grok API."""
        # Convert ChatMessage objects to dict format for xAI SDK
        messages_dict = []
        for msg in messages:
            # ChatMessage has role and content attributes
            role = getattr(msg, 'role', 'user')
            # Convert role to string if it's an enum or other type
            role_str = str(role) if role else 'user'
            # Handle common role mappings
            if role_str not in ['user', 'assistant', 'system']:
                role_str = 'user'  # Default fallback
            
            content = getattr(msg, 'content', str(msg))
            # Handle content that might be a list (for structured content)
            content_str = content if isinstance(content, str) else str(content)
            
            messages_dict.append({
                "role": role_str,
                "content": content_str
            })
        
        # xai-sdk Client uses sync methods, so we run in executor for async compatibility
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model=self.model_name,
                messages=messages_dict,
                temperature=self.temperature,
                stop=stop_sequences,
                **kwargs,
            )
        )
        
        # Return as ChatMessage
        content = response.choices[0].message.content or ""
        return ChatMessage(role="assistant", content=content)

