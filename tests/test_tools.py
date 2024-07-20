import pytest
from unittest.mock import AsyncMock, patch, Mock
from medhaai import AdvancedWebScraperTool, ToolKit
from medhaai.exceptions import WebScrapingError

@pytest.fixture
def mock_response():
    mock = AsyncMock()
    mock.__aenter__.return_value.status = 200
    mock.__aenter__.return_value.text.return_value = "<html><body><p>Test content</p></body></html>"
    return mock

@pytest.mark.asyncio
async def test_web_scraper(mock_response):
    with patch('aiohttp.ClientSession.get', return_value=mock_response):
        with patch('newspaper.Article') as mock_article:
            mock_article.return_value.title = "Test Title"
            mock_article.return_value.text = "Test content"
            mock_article.return_value.summary = "Test summary"
            mock_article.return_value.keywords = ["test", "keywords"]

            scraper = AdvancedWebScraperTool()
            result = await scraper.scrape("http://example.com")

            assert result['title'] == "Test Title"
            assert result['text'] == "Test content"
            assert result['summary'] == "Test summary"
            assert result['keywords'] == ["test", "keywords"]

@pytest.mark.asyncio
async def test_web_scraper_error():
    mock_response = AsyncMock()
    mock_response.__aenter__.return_value.status = 404
    
    with patch('aiohttp.ClientSession.get', return_value=mock_response):
        scraper = AdvancedWebScraperTool()
        with pytest.raises(WebScrapingError):
            await scraper.scrape("http://example.com")

@pytest.mark.asyncio
async def test_toolkit():
    toolkit = ToolKit()
    mock_result = {"result": "test"}
    with patch.object(AdvancedWebScraperTool, 'scrape', new_callable=AsyncMock, return_value=mock_result):
        result = await toolkit.use_tool("web_scraper", url="http://example.com")
        assert result == mock_result

    with pytest.raises(WebScrapingError):
        await toolkit.use_tool("non_existent_tool")