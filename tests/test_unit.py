import pytest
from medhaai import MedhaConfig, BaseLLM, BaseMemory, BasePlanner, BaseExecutor, BaseToolkit, BaseAgent

def test_medha_config():
    config = MedhaConfig(openai_api_key="test_key", default_model="gpt-3.5-turbo")
    assert config.openai_api_key == "test_key"
    assert config.default_model == "gpt-3.5-turbo"

@pytest.mark.asyncio
async def test_base_llm():
    llm = BaseLLM.create("openai", api_key="test_key")
    response = await llm.generate("Hello, world!")
    assert isinstance(response, str)

@pytest.mark.asyncio
async def test_base_memory():
    memory = BaseMemory.create("in_memory", capacity=100)
    await memory.store({"key": "value"})
    recent = await memory.retrieve_recent(1)
    assert len(recent) == 1
    assert recent[0]["key"] == "value"

@pytest.mark.asyncio
async def test_base_planner():
    llm = BaseLLM.create("openai", api_key="test_key")
    planner = BasePlanner.create("hierarchical", llm=llm)
    plan = await planner.create_plan("Write a story", "writer")
    assert isinstance(plan, dict)

@pytest.mark.asyncio
async def test_base_executor():
    executor = BaseExecutor.create("parallel", max_concurrent=5)
    result = await executor.execute_plan({"type": "action", "description": "Test action"})
    assert isinstance(result, dict)

def test_base_toolkit():
    toolkit = BaseToolkit.create_default()
    assert "web_scraper" in toolkit.tools
    assert "calculator" in toolkit.tools

@pytest.mark.asyncio
async def test_base_agent():
    llm = BaseLLM.create("openai", api_key="test_key")
    memory = BaseMemory.create("in_memory")
    planner = BasePlanner.create("hierarchical", llm=llm)
    executor = BaseExecutor.create("parallel")
    toolkit = BaseToolkit.create_default()
    agent = BaseAgent.create(
        "general",
        name="TestAgent",
        role="assistant",
        llm=llm,
        memory=memory,
        planner=planner,
        executor=executor,
        toolkit=toolkit
    )
    result = await agent.run("Hello, world!")
    assert isinstance(result, str)