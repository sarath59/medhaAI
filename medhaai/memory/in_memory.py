from .base import BaseMemory
from typing import Dict, Any, List

class InMemoryMemory(BaseMemory):
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.memory: List[Dict[str, Any]] = []

    async def store(self, item: Dict[str, Any]) -> None:
        self.memory.append(item)
        if len(self.memory) > self.capacity:
            self.memory.pop(0)

    async def retrieve_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.memory[-limit:]

    async def search(self, query: str) -> List[Dict[str, Any]]:
        # Simple search implementation
        return [item for item in self.memory if query.lower() in str(item).lower()]

    async def clear(self) -> None:
        self.memory.clear()