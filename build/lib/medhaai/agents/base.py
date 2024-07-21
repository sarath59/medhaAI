from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..llm.base import BaseLLM
from ..memory.base import BaseMemory
from ..planning.base import BasePlanner
from ..execution.base import BaseExecutor
from ..tools.base import BaseToolkit
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, llm: BaseLLM, memory: BaseMemory, planner: BasePlanner, executor: BaseExecutor, toolkit: BaseToolkit):
        self.name = name
        self.role = role
        self.llm = llm
        self.memory = memory
        self.planner = planner
        self.executor = executor
        self.toolkit = toolkit

    @abstractmethod
    async def run(self, task: str, collaborators: List['BaseAgent'] = None) -> str:
        pass

    @abstractmethod
    async def collaborate(self, message: str, sender: 'BaseAgent') -> str:
        pass

    @classmethod
    def create(cls, agent_type: str, **kwargs):
        if agent_type == "general":
            return cls(**kwargs)
        elif agent_type == "specialized":
            from .specialized_agents import SpecializedAgent
            return SpecializedAgent(**kwargs)
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")