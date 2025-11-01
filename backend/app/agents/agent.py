from typing import List
from smolagents import CodeAgent, Tool
from ..infrastructure.settings import settings
from ..infrastructure.models.grok_model import GrokModel
from .tools.nppes_tool import NppesTool
from .tools.web_search_tool import WebSearchTool


def build_agent() -> CodeAgent:
    tools: List[Tool] = [NppesTool(), WebSearchTool()]
    
    # Initialize Grok model if API key is available
    model = None
    if settings.grok_api_key:
        try:
            model = GrokModel(api_key=settings.grok_api_key, model_name="grok-beta", temperature=0.7)
        except Exception as e:
            # Log error but continue with default model if Grok fails
            import logging
            logging.warning(f"Failed to initialize Grok model: {e}. Using default model.")
    
    # CodeAgent will use the Grok model if available, otherwise fallback to default behavior
    agent = CodeAgent(tools=tools, model=model, name="coordinator")
    return agent


