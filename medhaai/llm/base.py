from abc import ABC, abstractmethod
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        pass

    @classmethod
    def create(cls, llm_type: str, **kwargs):
        if llm_type == "openai":
            from .openai_llm import OpenAILLM
            return OpenAILLM(**kwargs)
        elif llm_type == "anthropic":
            from .anthropic_llm import AnthropicLLM
            return AnthropicLLM(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")