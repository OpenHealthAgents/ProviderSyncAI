from typing import Optional, Type, Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ...infrastructure.nppes import client as nppes_client

class NppesSearchInput(BaseModel):
    first_name: Optional[str] = Field(default=None, description="Provider's first name")
    last_name: Optional[str] = Field(default=None, description="Provider's last name")
    organization_name: Optional[str] = Field(default=None, description="Organization name")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State abbreviation")
    postal_code: Optional[str] = Field(default=None, description="Postal code")
    taxonomy: Optional[str] = Field(default=None, description="Taxonomy description")
    limit: int = Field(default=10, description="Number of results to return")

class NppesTool(BaseTool):
    name: str = "nppes_search"
    description: str = "Search NPPES for providers by name, location, or specialty."
    args_schema: Type[BaseModel] = NppesSearchInput

    def _run(self, **kwargs: Any) -> Any:
        # Sync version not implemented (or use async_to_sync)
        raise NotImplementedError("Use async run instead")
    
    async def _arun(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        taxonomy: Optional[str] = None,
        limit: int = 10,
        **kwargs: Any
    ) -> Any:
        return await nppes_client.search(
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
            city=city,
            state=state,
            postal_code=postal_code,
            taxonomy=taxonomy,
            limit=limit,
        )


