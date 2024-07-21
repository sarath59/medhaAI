from .base import BaseTool
import aiohttp
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urljoin
from typing import Dict, Any, List
import json

class WebScraperTool(BaseTool):
    async def run(self, url: str, depth: int = 1, max_pages: int = 5) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            return await self._scrape_recursive(session, url, depth, max_pages)

    async def _scrape_recursive(self, session: aiohttp.ClientSession, url: str, depth: int, max_pages: int, visited: set = None) -> Dict[str, Any]:
        if visited is None:
            visited = set()
        
        if url in visited or len(visited) >= max_pages or depth <= 0:
            return {}

        visited.add(url)
        
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return {"error": f"Failed to fetch {url}. Status code: {response.status}"}

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract main content using trafilatura
                extracted = trafilatura.extract(html)

                # Extract metadata
                metadata = self._extract_metadata(soup)

                # Extract links
                links = self._extract_links(soup, url)

                # Recursively scrape linked pages
                sub_pages = {}
                if depth > 1:
                    for link in links[:max_pages - len(visited)]:
                        sub_page = await self._scrape_recursive(session, link, depth - 1, max_pages, visited)
                        if sub_page:
                            sub_pages[link] = sub_page

                return {
                    "url": url,
                    "title": metadata.get("title", ""),
                    "description": metadata.get("description", ""),
                    "main_content": extracted,
                    "metadata": metadata,
                    "links": links,
                    "sub_pages": sub_pages
                }

        except Exception as e:
            return {"error": f"Error scraping {url}: {str(e)}"}

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        metadata = {}
        metadata['title'] = soup.title.string if soup.title else ""

        for meta in soup.find_all('meta'):
            if 'name' in meta.attrs and 'content' in meta.attrs:
                metadata[meta['name'].lower()] = meta['content']

        return metadata

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        links = []
        for a in soup.find_all('a', href=True):
            link = urljoin(base_url, a['href'])
            if link.startswith('http'):  # Only include web URLs
                links.append(link)
        return links

    async def search(self, query: str, search_engine: str = "https://www.google.com/search?q=") -> Dict[str, Any]:
        url = search_engine + query.replace(" ", "+")
        return await self.run(url)

    async def extract_structured_data(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        structured_data = []

        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                structured_data.append(data)
            except json.JSONDecodeError:
                pass

        return {"structured_data": structured_data}