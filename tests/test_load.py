import pytest
import asyncio
from medhaai import MedhaConfig, BaseLLM, BaseAgent, MedhaMultiAgentSystem

@pytest.mark.asyncio
async def test_multi_agent_system_load():
    config = MedhaConfig()
    llm = BaseLLM.create("openai", api_key="test_key")
    agent = BaseAgent.create("general", name="TestAgent", role="assistant", llm=llm)
    
    mas = MedhaMultiAgentSystem(task_decomposition_llm=llm)
    mas.add_agent(agent)
    
    num_tasks = 10
    tasks = ["Task " + str(i) for i in range(num_tasks)]
    
    async def run_task(task):
        return await mas.run_task(task)
    
    results = await asyncio.gather(*[run_task(task) for task in tasks])
    
    assert len(results) == num_tasks
    for result in results:
        assert isinstance(result, dict)
        assert "aggregated_result" in result

@pytest.mark.asyncio
async def test_live_stream_load():
    from medhaai.stream import LiveStream
    
    live_stream = LiveStream(speed='fast')
    num_messages = 1000
    
    async def push_messages():
        for i in range(num_messages):
            await live_stream.push(f"Message {i}")
    
    async def read_stream():
        count = 0
        async for _ in live_stream.get_stream():
            count += 1
            if count == num_messages:
                break
    
    push_task = asyncio.create_task(push_messages())
    read_task = asyncio.create_task(read_stream())
    
    await asyncio.gather(push_task, read_task)

@pytest.mark.asyncio
async def test_performance_monitor_load():
    from medhaai.utils import PerformanceMonitor
    
    monitor = PerformanceMonitor()
    num_tasks = 1000
    
    for i in range(num_tasks):
        monitor.start_task(f"Task{i}")
        await asyncio.sleep(0.001)  # Simulate short task
        monitor.end_task(f"Task{i}")
    
    report = monitor.generate_report()
    assert len(report["task_details"]) == num_tasks