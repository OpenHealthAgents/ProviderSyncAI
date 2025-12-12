"""Web scraping tool for provider websites."""
from typing import Optional, Type, Any
import re
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from ...infrastructure.http import get
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)

class WebScrapingInput(BaseModel):
    url: str = Field(..., description="URL to scrape")

class WebScrapingTool(BaseTool):
    """Scrape provider website for contact information."""
    
    name: str = "web_scrape_provider"
    description: str = "Scrape a provider's website for contact information, phone, email, address, and services"
    args_schema: Type[BaseModel] = WebScrapingInput
    
    def _run(self, **kwargs: Any) -> Any:
        raise NotImplementedError("Use async run instead")
    
    async def _arun(self, url: str) -> Any:
        """Scrape provider website."""
        try:
            resp = await get(url)
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            
            data = {
                "url": url,
                "phone": self._extract_phone(soup, html),
                "email": self._extract_email(soup, html),
                "address": self._extract_address(soup, html),
                "services": self._extract_services(soup),
            }
            
            return data
        except Exception as e:
            logger.warning("web_scraping_failed", url=url, error=str(e))
            return {"url": url, "error": str(e)}
    
    def _extract_phone(self, soup: BeautifulSoup, html: str) -> Optional[str]:
        """Extract phone number."""
        import re
        # Look for phone patterns
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, html)
        if phones:
            return phones[0]
        
        # Look for common phone selectors
        for tag in soup.find_all(['a', 'span', 'div'], class_=re.compile(r'phone|tel', re.I)):
            text = tag.get_text()
            match = re.search(phone_pattern, text)
            if match:
                return match.group()
        return None
    
    def _extract_email(self, soup: BeautifulSoup, html: str) -> Optional[str]:
        """Extract email address."""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        if emails:
            # Filter out common non-contact emails
            filtered = [e for e in emails if 'example' not in e.lower() and 'noreply' not in e.lower()]
            return filtered[0] if filtered else emails[0]
        return None
    
    def _extract_address(self, soup: BeautifulSoup, html: str) -> Optional[str]:
        """Extract address."""
        # Look for address in structured data
        for tag in soup.find_all(['address', 'div', 'span'], class_=re.compile(r'address|location', re.I)):
            text = tag.get_text().strip()
            if len(text) > 20 and any(char.isdigit() for char in text):
                return text
        return None
    
    def _extract_services(self, soup: BeautifulSoup) -> list:
        """Extract services offered."""
        services = []
        # Look for common service sections
        for tag in soup.find_all(['div', 'section', 'ul'], class_=re.compile(r'service|specialty|treatment', re.I)):
            for item in tag.find_all(['li', 'span', 'div']):
                text = item.get_text().strip()
                if text and len(text) > 3 and len(text) < 100:
                    services.append(text)
        return services[:10]  # Limit to top 10

