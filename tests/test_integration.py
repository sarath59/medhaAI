import pytest
from medhaai import MedhaConfig, BaseLLM, BaseAgent, MedhaMultiAgentSystem

@pytest.mark.asyncio
async def test_multi_agent_system():
    config = MedhaConfig()
    llm = BaseLLM.create("openai", api_key="test_key")
    agent1 = BaseAgent.create("general", name="Agent1", role="assistant", llm=llm)
    agent2 = BaseAgent.create("general", name="Agent2", role="researcher", llm=llm)
    
    mas = MedhaMultiAgentSystem(task_decomposition_llm=llm)
    mas.add_agent(agent1, priority=1)
    mas.add_agent(agent2, priority=2)
    
    result = await mas.run_task("Summarize the benefits of AI")
    assert isinstance(result, dict)
    assert "aggregated_result" in result
    assert isinstance(result["aggregated_result"], str)

@pytest.mark.asyncio
async def test_live_stream():
    from medhaai.stream import LiveStream
    
    live_stream = LiveStream(speed='fast')
    test_data = "Test data"
    
    await live_stream.push(test_data)
    
    async for data in live_stream.get_stream():
        assert data == test_data
        break

@pytest.mark.asyncio
async def test_performance_monitoring():
    from medhaai.utils import PerformanceMonitor
    
    monitor = PerformanceMonitor()
    monitor.start_task("TestTask")
    # Simulate task execution
    import asyncio
    await asyncio.sleep(1)
    monitor.end_task("TestTask")
    
    report = monitor.generate_report()
    assert "performance_data" in report
    assert "task_details" in report
    assert len(report["task_details"]) == 1
    assert report["task_details"][0]["task"] == "TestTask"