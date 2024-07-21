from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class BaseExecutor(ABC):
    @abstractmethod
    async def execute_plan(self, plan: Dict[str, Any], collaborators: List['BaseAgent'] = None) -> Dict[str, Any]:
        pass

    @classmethod
    def create(cls, executor_type: str, **kwargs):
        if executor_type == "parallel":
            from .parallel import ParallelExecutor
            return ParallelExecutor(**kwargs)
        else:
            raise ValueError(f"Unsupported executor type: {executor_type}")