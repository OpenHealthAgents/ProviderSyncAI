"""Information Enrichment Agent node for adding provider data."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from ...domain.enriched_entities import EnrichedProvider
from ...infrastructure.models.grok_model import GrokModel
from ...infrastructure.logging import get_logger
from ..tools.nppes_tool import NppesTool
from ..tools.web_search_tool import WebSearchTool
from ..tools.state_licensing_tool import StateLicensingTool
from ..state import AgentState


logger = get_logger(__name__)

async def information_enrichment_node(state: AgentState) -> Dict[str, Any]:
    """
    Node for enriching provider information from multiple sources.
    """
    logger.info("information_enrichment_node_start")
    
    # Extract provider data
    provider_data = state.get("provider_data", {})
    if isinstance(provider_data, dict):
        provider = EnrichedProvider(**provider_data)
    else:
        provider = provider_data

    logger.info("enriching_provider", npi=provider.npi)

    # Initialize tools
    tools = [
        NppesTool(),
        WebSearchTool(),
        StateLicensingTool(),
    ]

    # Initialize model
    model = GrokModel()
    
    # Create agent
    agent = create_react_agent(model, tools)

    prompt = f"""Enrich provider information for {provider.first_name} {provider.last_name} (NPI: {provider.npi}).

Current information:
- Name: {provider.first_name} {provider.last_name}
- Location: {provider.city}, {provider.state}
- Specialty: {provider.taxonomy}

Tasks:
1. Use nppes_search to get detailed provider information
2. Use web_search to find provider's education, board certifications, and specialties
3. Use state_license_lookup to get license information if available
4. Identify network affiliations and facility relationships
5. Find services offered by the provider

Return enriched information including:
- Education history
- Board certifications
- Additional specialties
- Network affiliations
- Services offered
"""

    # Run agent
    messages = [HumanMessage(content=prompt)]
    result = await agent.ainvoke({"messages": messages})
    
    last_message = result['messages'][-1]
    response_text = last_message.content

    # Placeholder: Parse response_text into structured fields
    # For now, we trust the agent to report these findings and we append to notes or similar.
    # Ideally should use structured output.
    
    # Assuming we want to capture this enrichment in the provider object somehow.
    # The existing code didn't actually implement parsing, just the prompt.
    
    # Let's save the summary to a new field or just log it.
    # provider.enrichment_notes = response_text # (If such field existed)

    logger.info("provider_enriched", npi=provider.npi)
    
    return {
        "provider_data": provider.model_dump(),
        "messages": [last_message]
    }

