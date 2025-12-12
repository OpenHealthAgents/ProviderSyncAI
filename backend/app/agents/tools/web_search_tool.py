from typing import Type, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ...infrastructure.searxng import client as searxng_client

class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    categories: str = Field(default="general", description="Comma-separated categories")
    num_results: int = Field(default=5, description="Number of results to return")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web via SearXNG and return top results."
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, categories: str = "general", num_results: int = 5) -> Any:
        raise NotImplementedError("Use async run instead")
    
    async def _arun(self, query: str, categories: str = "general", num_results: int = 5) -> Any:
        return await searxng_client.search(query, categories=categories, num_results=num_results)


