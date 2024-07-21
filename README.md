# MedhaAI

MedhaAI is a flexible and powerful multi-agent AI framework for building advanced AI applications. It provides a set of tools and abstractions that allow developers to create complex, collaborative AI systems with ease.

## Features

- Multi-agent system with prioritized agents
- Support for multiple LLM providers (OpenAI, Anthropic)
- Flexible memory systems
- Advanced planning and execution modules
- Customizable toolkit system with advanced web scraping capabilities
- Live streaming of agent activities
- Performance monitoring and tracing
- Asynchronous operations for improved performance

## Installation

To install MedhaAI, simply use pip:

```bash
pip install medhaai
```

## Quick Start

Here's a simple example to get you started with MedhaAI:

```python
import asyncio
from medhaai import MedhaConfig, BaseLLM, BaseAgent, MedhaMultiAgentSystem

async def main():
    config = MedhaConfig()
    llm = BaseLLM.create("openai", api_key=config.openai_api_key)
    agent = BaseAgent.create("general", name="GeneralAgent", role="assistant", llm=llm)
    mas = MedhaMultiAgentSystem(task_decomposition_llm=llm)
    mas.add_agent(agent)
    result = await mas.run_task("Research and summarize the latest advancements in quantum computing")
    print(result)

asyncio.run(main())
```

## Documentation

For more detailed information and advanced usage, please refer to our [documentation](https://medhaai.readthedocs.io).

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.