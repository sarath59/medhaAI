from setuptools import setup, find_packages

setup(
    name="medhaai",
    version="0.3.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.3.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "aiohttp>=3.7.4",
        "beautifulsoup4>=4.9.3",
        "newspaper3k>=0.2.8",
        "nltk>=3.6.2",
        "lxml>=4.6.3",
    ],
)