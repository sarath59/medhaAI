import pytest
from medhaai import MedhaConfig

def test_config_validation():
    config = MedhaConfig(openai_api_key="test_key", llm_model_name="gpt-3.5-turbo")
    assert config.llm_model_name == "gpt-3.5-turbo"
    assert config.max_tokens == 500
    assert config.temperature == 0.7

def test_config_env_variables(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_env_key")
    monkeypatch.setenv("MEDHA_MODEL_NAME", "gpt-4")
    monkeypatch.setenv("MEDHA_MAX_TOKENS", "1000")
    
    config = MedhaConfig()
    assert config.openai_api_key == "test_env_key"
    assert config.llm_model_name == "gpt-4"
    assert config.max_tokens == 1000