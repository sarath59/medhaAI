import asyncio
import os
from medhaai import MedhaConfig, MedhaLLM, ToolKit, AdvancedWebScraperTool, MedhaAgent

async def main():
    # Set up configuration
    config = MedhaConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        llm_model_name="gpt-3.5-turbo",
        max_tokens=300,
        temperature=0.7
    )

    # Initialize LLM
    llm = MedhaLLM(config)

    # Initialize ToolKit with web scraper
    toolkit = ToolKit()
    toolkit.tools["web_scraper"] = AdvancedWebScraperTool().scrape

    # Initialize Agent
    agent = MedhaAgent(llm, toolkit)

    # Define a task for the agent
    task = "Research the latest advancements in quantum computing and summarize the key findings."

    try:
        # Run the agent
        result = await agent.run(task)
        
        print("Agent's Summary:")
        print(result)
        
    except Exception as e:
        print(f"Error during agent execution: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())