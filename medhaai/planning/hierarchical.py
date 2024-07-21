from .base import BasePlanner
from ..llm.base import BaseLLM
from typing import Dict, Any

class HierarchicalPlanner(BasePlanner):
    def __init__(self, llm: BaseLLM, max_depth: int = 3):
        self.llm = llm
        self.max_depth = max_depth

    async def create_plan(self, task: str, role: str) -> Dict[str, Any]:
        prompt = f"As a {role}, create a hierarchical plan for the task: {task}. Break it down into subtasks if necessary."
        raw_plan = await self.llm.generate(prompt)
        return self._structure_plan(raw_plan)

    async def optimize_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        # In a real implementation, this would optimize the plan
        return plan

    def _structure_plan(self, raw_plan: str) -> Dict[str, Any]:
        # This is a simplified implementation. In a real scenario, you'd parse the raw_plan more robustly.
        lines = raw_plan.strip().split('\n')
        if len(lines) == 1:
            return {"type": "action", "description": lines[0]}
        else:
            return {"type": "composite", "subtasks": [{"type": "action", "description": line} for line in lines]}