import asyncio
from openai import AsyncOpenAI, RateLimitError
from anthropic import AsyncAnthropic
from .config import MedhaConfig
from .exceptions import LLMError, UnsupportedModelError
from .logging import setup_logger

logger = setup_logger(__name__)

class MedhaLLM:
    def __init__(self, config: MedhaConfig):
        self.config = config
        if 'gpt' in config.llm_model_name:
            self.client = AsyncOpenAI(api_key=config.openai_api_key)
            self.provider = 'openai'
        elif 'claude' in config.llm_model_name:
            if not config.anthropic_api_key:
                raise UnsupportedModelError("Anthropic API key is required for Claude models")
            self.client = AsyncAnthropic(api_key=config.anthropic_api_key)
            self.provider = 'anthropic'
        else:
            raise UnsupportedModelError(f"Unsupported model: {config.llm_model_name}")

    async def generate(self, prompt: str) -> str:
        for attempt in range(self.config.max_retries):
            try:
                if self.provider == 'openai':
                    return await self._generate_openai(prompt)
                elif self.provider == 'anthropic':
                    return await self._generate_anthropic(prompt)
            except RateLimitError:
                if attempt == self.config.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logger.error(f"Error in LLM generation: {str(e)}")
                if attempt == self.config.max_retries - 1:
                    raise LLMError(f"Error in LLM generation: {str(e)}")
        raise LLMError("Max retries reached")

    async def _generate_openai(self, prompt: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                model=self.config.llm_model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise LLMError(f"OpenAI API error: {str(e)}")

    async def _generate_anthropic(self, prompt: str) -> str:
        try:
            completion = await self.client.completions.create(
                model=self.config.llm_model_name,
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
                max_tokens_to_sample=self.config.max_tokens,
                temperature=self.config.temperature
            )
            return completion.completion
        except Exception as e:
            raise LLMError(f"Anthropic API error: {str(e)}")