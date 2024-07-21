from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="medhaai",
    version="0.4.0",
    author="Sarath Kavuru",
    author_email="sarathc225@gmail.com",
    description="A flexible and powerful multi-agent AI framework for building advanced AI applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sarath59/medhaAI",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "openai>=1.0.0",
        "anthropic>=0.3.0",
        "aiohttp>=3.7.4",
        "beautifulsoup4>=4.9.3",
        "trafilatura>=1.4.0",
        "opentelemetry-api>=1.12.0",
        "opentelemetry-sdk>=1.12.0",
        "asyncio>=3.4.3",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-asyncio>=0.15.1",
            "black>=21.9b0",
            "isort>=5.9.3",
        ],
    },
)