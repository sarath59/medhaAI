from abc import ABC, abstractmethod
from typing import Dict, Any
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class BaseTool(ABC):
    @abstractmethod
    async def run(self, **kwargs) -> Any:
        pass

class BaseToolkit:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def add_tool(self, name: str, tool: BaseTool) -> None:
        self.tools[name] = tool
        logger.info(f"Added tool {name} to the toolkit")

    async def use_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        return await self.tools[tool_name].run(**kwargs)

    @classmethod
    def create_default(cls):
        toolkit = cls()
        from .web_scraper import WebScraperTool
        from .calculator import CalculatorTool
        toolkit.add_tool("web_scraper", WebScraperTool())
        toolkit.add_tool("calculator", CalculatorTool())
        return toolkit