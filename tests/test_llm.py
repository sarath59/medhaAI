import pytest
from unittest.mock import AsyncMock, patch, Mock
from medhaai import MedhaConfig, MedhaLLM
from medhaai.exceptions import UnsupportedModelError, LLMError
from openai import RateLimitError, APIError

@pytest.fixture
def config():
    return MedhaConfig(openai_api_key="test_key", llm_model_name="gpt-3.5-turbo")

@pytest.mark.asyncio
async def test_llm_generation(config):
    with patch('openai.AsyncOpenAI') as mock_openai:
        mock_completion = Mock()
        mock_completion.choices = [Mock(message=Mock(content="Test response"))]
        mock_openai.return_value.chat.completions.create = AsyncMock(return_value=mock_completion)
        llm = MedhaLLM(config)
        response = await llm.generate("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_unsupported_model():
    with pytest.raises(UnsupportedModelError):
        config = MedhaConfig(openai_api_key="test_key", llm_model_name="unsupported-model")
        MedhaLLM(config)

@pytest.mark.asyncio
async def test_rate_limit_retry(config):
    with patch('openai.AsyncOpenAI') as mock_openai:
        mock_completion = Mock()
        mock_completion.choices = [Mock(message=Mock(content="Test response"))]
        mock_openai.return_value.chat.completions.create = AsyncMock(side_effect=[
            RateLimitError("Rate limit exceeded", response=Mock(status_code=429)),
            mock_completion
        ])
        llm = MedhaLLM(config)
        response = await llm.generate("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_max_retries_exceeded(config):
    with patch('openai.AsyncOpenAI') as mock_openai:
        mock_openai.return_value.chat.completions.create = AsyncMock(side_effect=APIError("API Error"))
        llm = MedhaLLM(config)
        with pytest.raises(LLMError):
            await llm.generate("Test prompt")