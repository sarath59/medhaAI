from .base import BaseAgent
from ..llm.base import BaseLLM
from ..memory.base import BaseMemory
from ..planning.base import BasePlanner
from ..execution.base import BaseExecutor
from ..tools.base import BaseToolkit
from typing import List

class SpecializedAgent(BaseAgent):
    def __init__(self, name: str, role: str, llm: BaseLLM, memory: BaseMemory, planner: BasePlanner, executor: BaseExecutor, toolkit: BaseToolkit):
        super().__init__(name, role, llm, memory, planner, executor, toolkit)

    async def run(self, task: str, collaborators: List['BaseAgent'] = None) -> str:
        plan = await self.planner.create_plan(task, self.role)
        result = await self.executor.execute_plan(plan, collaborators)
        summary = await self.llm.generate(f"Summarize the following result: {result}")
        await self.memory.store({"task": task, "result": summary})
        return summary

    async def collaborate(self, message: str, sender: 'BaseAgent') -> str:
        response = await self.llm.generate(f"As {self.role}, respond to this message from {sender.name}: {message}")
        return response