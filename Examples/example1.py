import asyncio
from medhaai import (
    MedhaConfig,
    BaseLLM,
    BaseMemory,
    BasePlanner,
    BaseExecutor,
    BaseToolkit,
    BaseAgent,
    MedhaMultiAgentSystem,
    LiveStream,
    PerformanceMonitor,
    Tracer
)
from medhaai.logging_utils import setup_logger

logger = setup_logger(__name__)

async def print_live_stream(live_stream: LiveStream):
    async for data in live_stream.get_stream():
        print(f"Live Stream: {data}")

async def main():
    # Load configuration
    config = MedhaConfig()

    # Create LLM instances
    openai_llm = BaseLLM.create("openai", api_key=config.openai_api_key, model=config.default_model)
    anthropic_llm = BaseLLM.create("anthropic", api_key=config.anthropic_api_key, model="claude-2")

    # Create memory instances
    in_memory = BaseMemory.create("in_memory", capacity=config.memory_capacity)
    db_memory = BaseMemory.create("database", db_url=config.db_url)

    # Create planner and executor instances
    planner = BasePlanner.create("hierarchical", llm=openai_llm, max_depth=config.planning_max_depth)
    executor = BaseExecutor.create("parallel", max_concurrent=config.execution_max_concurrent)

    # Create toolkit instances
    toolkit = BaseToolkit.create_default()

    # Create specialized agents
    web_scraper_agent = BaseAgent.create(
        "specialized",
        name="WebScraperAgent",
        role="web_scraper",
        llm=openai_llm,
        memory=in_memory,
        planner=planner,
        executor=executor,
        toolkit=toolkit
    )

    data_analyst_agent = BaseAgent.create(
        "specialized",
        name="DataAnalystAgent",
        role="data_analyst",
        llm=anthropic_llm,
        memory=db_memory,
        planner=planner,
        executor=executor,
        toolkit=toolkit
    )

    summarizer_agent = BaseAgent.create(
        "specialized",
        name="SummarizerAgent",
        role="summarizer",
        llm=openai_llm,
        memory=in_memory,
        planner=planner,
        executor=executor,
        toolkit=toolkit
    )

    # Create multi-agent system with custom settings
    mas = MedhaMultiAgentSystem(
        task_decomposition_llm=openai_llm,
        enable_performance_monitoring=True,
        enable_tracing=True,
        stream_speed='fast'  # Set initial stream speed
    )
    
    mas.add_agent(web_scraper_agent, priority=2)  # Highest priority
    mas.add_agent(data_analyst_agent, priority=1)
    mas.add_agent(summarizer_agent, priority=0)  # Lowest priority

    # Start live streaming
    stream_task = asyncio.create_task(print_live_stream(mas.live_stream))

    # Define a complex task
    task = "Research the latest advancements in quantum computing, analyze their potential impact on cryptography, and provide a summarized report."

    try:
        # Run the task
        result = await mas.run_task(task, timeout=600)  # 10 minutes timeout
        
        print("Task Result:")
        print(result['aggregated_result'])

        # Get performance report
        performance_report = mas.get_performance_report()
        print("\nPerformance Report:")
        print(performance_report['summary'])

    except Exception as e:
        logger.error(f"Error during task execution: {str(e)}")
        if mas.tracer:
            mas.tracer.log_error("TaskExecutionError", str(e), "")

    # Change stream speed mid-execution
    mas.set_stream_speed('slow')

    # Stop live streaming
    stream_task.cancel()
    try:
        await stream_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())