from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class BaseMemory(ABC):
    @abstractmethod
    async def store(self, item: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def retrieve_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass

    @classmethod
    def create(cls, memory_type: str, **kwargs):
        if memory_type == "in_memory":
            from .in_memory import InMemoryMemory
            return InMemoryMemory(**kwargs)
        elif memory_type == "database":
            from .database import DatabaseMemory
            return DatabaseMemory(**kwargs)
        else:
            raise ValueError(f"Unsupported memory type: {memory_type}")