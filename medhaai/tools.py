from typing import Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from newspaper import Article
import nltk
from .exceptions import WebScrapingError
from .logging import setup_logger

logger = setup_logger(__name__)

nltk.download('punkt', quiet=True)

class AdvancedWebScraperTool:
    async def scrape(self, url: str) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        return await self._process_html(html, url)
                    else:
                        logger.error(f"Failed to fetch URL: {url}. Status code: {response.status}")
                        raise WebScrapingError(f"Failed to fetch URL: {url}. Status code: {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error during web scraping: {str(e)}")
            raise WebScrapingError(f"Network error during web scraping: {str(e)}")
        except Exception as e:
            logger.error(f"Error during web scraping: {str(e)}")
            raise WebScrapingError(f"Error during web scraping: {str(e)}")

    async def _process_html(self, html: str, url: str) -> Dict[str, Any]:
        try:
            article = Article(url)
            article.set_html(html)
            article.parse()
            article.nlp()

            soup = BeautifulSoup(html, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]

            return {
                'title': article.title,
                'text': article.text[:1000],
                'summary': article.summary,
                'keywords': article.keywords,
                'links': links[:10]
            }
        except Exception as e:
            logger.error(f"Error processing HTML: {str(e)}")
            raise WebScrapingError(f"Error processing HTML: {str(e)}")

class ToolKit:
    def __init__(self):
        self.tools: Dict[str, Any] = {
            "web_scraper": AdvancedWebScraperTool().scrape
        }

    async def use_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            logger.error(f"Tool {tool_name} not found")
            raise WebScrapingError(f"Tool {tool_name} not found")
        return await self.tools[tool_name](**kwargs)