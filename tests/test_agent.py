import pytest
from unittest.mock import AsyncMock, patch
from medhaai import MedhaAgent, MedhaLLM, ToolKit, MedhaConfig

@pytest.fixture
def mock_llm():
    return AsyncMock(spec=MedhaLLM)

@pytest.fixture
def mock_toolkit():
    return AsyncMock(spec=ToolKit)

@pytest.fixture
def agent(mock_llm, mock_toolkit):
    return MedhaAgent(mock_llm, mock_toolkit)

@pytest.mark.asyncio
async def test_agent_run(agent, mock_llm, mock_toolkit):
    mock_llm.generate.side_effect = [
        "1. Step 1\n2. web_scraper: http://example.com\n3. Step 3",
        "Result 1",
        "Result 3",
        "Final summary"
    ]
    mock_toolkit.use_tool.return_value = {"result": "Scraped data"}

    result = await agent.run("Test task")

    assert result == "Final summary"
    assert mock_llm.generate.call_count == 4
    assert mock_toolkit.use_tool.call_count == 1

@pytest.mark.asyncio
async def test_agent_error_handling(agent, mock_llm):
    mock_llm.generate.side_effect = Exception("Test error")

    with pytest.raises(Exception):
        await agent.run("Test task")

@pytest.mark.asyncio
async def test_agent_context_update(agent):
    await agent.update_context({"key": "value"})
    assert agent.context == {"key": "value"}