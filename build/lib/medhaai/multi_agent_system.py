import asyncio
from typing import Dict, Any, List
from .agents.base import BaseAgent
from .llm.base import BaseLLM
from .logging_utils import setup_logger
from .exceptions import MultiAgentSystemError
from .utils.performance_monitoring import PerformanceMonitor
from .utils.tracing import Tracer
from .stream.live_stream import LiveStream

logger = setup_logger(__name__)

class MedhaMultiAgentSystem:
    def __init__(self, 
                 task_decomposition_llm: BaseLLM = None, 
                 enable_performance_monitoring: bool = True,
                 enable_tracing: bool = True,
                 stream_speed: str = 'medium'):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.task_decomposition_llm = task_decomposition_llm
        self.performance_monitor = PerformanceMonitor() if enable_performance_monitoring else None
        self.tracer = Tracer() if enable_tracing else None
        self.live_stream = LiveStream(speed=stream_speed)

    def add_agent(self, agent: BaseAgent, priority: int = 0) -> None:
        self.agents[agent.name] = {"agent": agent, "priority": priority}
        logger.info(f"Added agent {agent.name} to the multi-agent system with priority {priority}")

    async def run_task(self, task: str, timeout: float = 300.0) -> Dict[str, Any]:
        try:
            logger.info(f"Starting task: {task}")
            if self.performance_monitor:
                self.performance_monitor.start_task(task)

            subtasks = await self._decompose_task(task)
            results = await asyncio.wait_for(self._execute_subtasks(subtasks), timeout=timeout)
            final_result = await self._aggregate_results(results)

            if self.performance_monitor:
                self.performance_monitor.end_task(task)

            logger.info("Task completed successfully")
            return final_result
        except asyncio.TimeoutError:
            logger.error(f"Task execution timed out after {timeout} seconds")
            raise MultiAgentSystemError(f"Task execution timed out after {timeout} seconds")
        except Exception as e:
            logger.error(f"Error in multi-agent task execution: {str(e)}")
            raise MultiAgentSystemError(f"Error in multi-agent task execution: {str(e)}")

    async def _decompose_task(self, task: str) -> List[Dict[str, Any]]:
        if not self.task_decomposition_llm:
            return [{"agent": list(self.agents.keys())[0], "task": task}]
        
        prompt = f"Decompose the following task into subtasks, assigning each to the most suitable agent: {task}\n\nAvailable agents: {', '.join(self.agents.keys())}"
        raw_decomposition = await self.task_decomposition_llm.generate(prompt)
        subtasks = [{"agent": line.split(':')[0].strip(), "task": line.split(':')[1].strip()} for line in raw_decomposition.split('\n') if ':' in line]
        logger.info(f"Decomposed task into {len(subtasks)} subtasks")
        return subtasks

    async def _execute_subtasks(self, subtasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        sorted_agents = sorted(self.agents.items(), key=lambda x: x[1]["priority"], reverse=True)
        results = []
        for subtask in subtasks:
            for agent_name, agent_info in sorted_agents:
                if agent_name == subtask['agent']:
                    agent = agent_info["agent"]
                    if self.tracer:
                        self.tracer.log_agent_interaction(agent_name, "start_subtask", input_data=subtask['task'])
                    result = await agent.run(subtask['task'], list(a["agent"] for a in self.agents.values()))
                    if self.tracer:
                        self.tracer.log_agent_interaction(agent_name, "end_subtask", output_data=str(result))
                    results.append({
                        'agent': agent_name,
                        'task': subtask['task'],
                        'result': result
                    })
                    await self.live_stream.push(f"Agent {agent_name} completed task: {subtask['task'][:50]}...")
                    break
        return results

    async def _aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        aggregated_result = '\n'.join([f"{r['agent']}: {r['result']}" for r in results])
        await self.live_stream.push(f"Aggregated result: {aggregated_result[:100]}...")
        return {
            'aggregated_result': aggregated_result,
            'individual_results': results
        }

    async def monitor_performance(self, interval: float = 60.0) -> None:
        if not self.performance_monitor:
            logger.warning("Performance monitoring is disabled")
            return

        while True:
            performance_data = self.performance_monitor.get_performance_data()
            logger.info(f"Performance data collected: {performance_data}")
            await self.live_stream.push(f"Performance update: {performance_data}")
            await asyncio.sleep(interval)

    def get_performance_report(self) -> Dict[str, Any]:
        if not self.performance_monitor:
            logger.warning("Performance monitoring is disabled")
            return {}

        return self.performance_monitor.generate_report()

    def set_stream_speed(self, speed: str) -> None:
        self.live_stream.set_speed(speed)
        logger.info(f"Live stream speed set to: {speed}")

    def enable_performance_monitoring(self) -> None:
        if not self.performance_monitor:
            self.performance_monitor = PerformanceMonitor()
            logger.info("Performance monitoring enabled")

    def disable_performance_monitoring(self) -> None:
        if self.performance_monitor:
            self.performance_monitor = None
            logger.info("Performance monitoring disabled")

    def enable_tracing(self) -> None:
        if not self.tracer:
            self.tracer = Tracer()
            logger.info("Tracing enabled")

    def disable_tracing(self) -> None:
        if self.tracer:
            self.tracer = None
            logger.info("Tracing disabled")