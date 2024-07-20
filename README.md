# MedhaAI

MedhaAI is an advanced AI agent framework with minimal abstraction, designed for easy integration of language models and web scraping capabilities.

## Features

- Support for multiple LLM providers (OpenAI and Anthropic)
- Advanced web scraping tool
- Flexible agent system for complex task execution
- Built-in error handling and logging
- Easy configuration management

## Installation

```bash
pip install medhaai
```

## Quick Start

```python
import asyncio
from medhaai import MedhaConfig, MedhaLLM, MedhaAgent, ToolKit

async def main():
    config = MedhaConfig(
        openai_api_key="your_openai_api_key_here",
        model_name="gpt-3.5-turbo"
    )
    llm = MedhaLLM(config)
    toolkit = ToolKit()
    agent = MedhaAgent(llm, toolkit)
    
    result = await agent.run("Research the latest advancements in quantum computing")
    print(result)

asyncio.run(main())
```

## Documentation

For full documentation, visit [docs.medhaai.com](https://docs.medhaai.com).

## Advanced Usage

### Using Different LLM Providers

MedhaAI supports both OpenAI and Anthropic models. Here's how to use an Anthropic model:

```python
config = MedhaConfig(
    anthropic_api_key="your_anthropic_api_key_here",
    model_name="claude-2"
)
llm = MedhaLLM(config)
```

### Custom Web Scraping

You can use the web scraping tool directly:

```python
from medhaai import AdvancedWebScraperTool

scraper = AdvancedWebScraperTool()
result = await scraper.scrape("https://example.com")
print(result)
```

### Error Handling

MedhaAI provides custom exceptions for better error handling:

```python
from medhaai.exceptions import MedhaAIException

try:
    result = await agent.run("Some task")
except MedhaAIException as e:
    print(f"An error occurred: {str(e)}")
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.