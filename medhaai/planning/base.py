from abc import ABC, abstractmethod
from typing import Dict, Any
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class BasePlanner(ABC):
    @abstractmethod
    async def create_plan(self, task: str, role: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def optimize_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @classmethod
    def create(cls, planner_type: str, **kwargs):
        if planner_type == "hierarchical":
            from .hierarchical import HierarchicalPlanner
            return HierarchicalPlanner(**kwargs)
        else:
            raise ValueError(f"Unsupported planner type: {planner_type}")