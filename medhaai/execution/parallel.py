import asyncio
from typing import Dict, Any, List
from .base import BaseExecutor

class ParallelExecutor(BaseExecutor):
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent

    async def execute_plan(self, plan: Dict[str, Any], collaborators: List['BaseAgent'] = None) -> Dict[str, Any]:
        if plan['type'] == 'action':
            return await self._execute_action(plan['description'], collaborators)
        elif plan['type'] == 'composite':
            return await self._execute_composite(plan['subtasks'], collaborators)
        else:
            raise ValueError(f"Unknown plan type: {plan['type']}")

    async def _execute_action(self, action: str, collaborators: List['BaseAgent']) -> Dict[str, Any]:
        # This is a placeholder. In a real implementation, you'd have logic to execute the action.
        return {"result": f"Executed action: {action}"}

    async def _execute_composite(self, subtasks: List[Dict[str, Any]], collaborators: List['BaseAgent']) -> Dict[str, Any]:
        semaphore = asyncio.Semaphore(self.max_concurrent)
        async def execute_with_semaphore(subtask):
            async with semaphore:
                return await self.execute_plan(subtask, collaborators)
        
        results = await asyncio.gather(*[execute_with_semaphore(subtask) for subtask in subtasks])
        return {"results": results}