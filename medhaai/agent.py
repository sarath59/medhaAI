from typing import Dict, Any
from .llm import MedhaLLM
from .tools import ToolKit
from .exceptions import MedhaAIException
from .logging import setup_logger

logger = setup_logger(__name__)

class MedhaAgent:
    def __init__(self, llm: MedhaLLM, toolkit: ToolKit):
        self.llm = llm
        self.toolkit = toolkit

    async def run(self, task: str) -> str:
        try:
            logger.info(f"Starting task: {task}")
            
            # Generate a plan
            plan = await self.generate_plan(task)
            logger.info(f"Generated plan: {plan}")
            
            # Execute the plan
            result = await self.execute_plan(plan)
            logger.info("Plan execution completed")
            
            # Analyze and summarize the result
            summary = await self.analyze_and_summarize(result)
            logger.info("Task completed successfully")
            
            return summary
        except Exception as e:
            logger.error(f"Error in agent execution: {str(e)}")
            raise MedhaAIException(f"Error in agent execution: {str(e)}")

    async def generate_plan(self, task: str) -> str:
        prompt = f"Given the task: '{task}', create a step-by-step plan to accomplish it. If needed, use the web_scraper tool to gather information. Provide the plan in a numbered list format."
        return await self.llm.generate(prompt)

    async def execute_plan(self, plan: str) -> Dict[str, Any]:
        steps = plan.split('\n')
        results = {}
        for step in steps:
            logger.info(f"Executing step: {step}")
            if "web_scraper" in step.lower():
                url = step.split("web_scraper:")[-1].strip()
                results[step] = await self.toolkit.use_tool("web_scraper", url=url)
            else:
                results[step] = await self.llm.generate(step)
        return results

    async def analyze_and_summarize(self, results: Dict[str, Any]) -> str:
        prompt = "Analyze and summarize the following information:\n\n"
        for step, result in results.items():
            prompt += f"Step: {step}\nResult: {result}\n\n"
        prompt += "Provide a concise summary of the key findings and insights."
        return await self.llm.generate(prompt)