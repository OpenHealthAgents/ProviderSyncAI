from typing import TypedDict, Annotated, List, Union, Any, Dict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # The messages in the conversation
    messages: Annotated[List[BaseMessage], add_messages]
    # The next agent to act
    next: str
    # Context data (provider information being processed)
    # Using Any for now to avoid circular imports with EnrichedProvider, 
    # but ideally should be Dict or the Pydantic model dump
    provider_data: Dict[str, Any] 
    # Tracking which agents have run
    agents_run: Annotated[List[str], operator.add]
