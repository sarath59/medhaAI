from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class MedhaConfig(BaseSettings):
    openai_api_key: Optional[str] = Field(None, env='OPENAI_API_KEY')
    anthropic_api_key: Optional[str] = Field(None, env='ANTHROPIC_API_KEY')
    llm_model_name: str = Field('gpt-3.5-turbo', env='MEDHA_MODEL_NAME')
    max_tokens: int = Field(500, env='MEDHA_MAX_TOKENS')
    temperature: float = Field(0.7, env='MEDHA_TEMPERATURE')
    request_timeout: int = Field(30, env='MEDHA_REQUEST_TIMEOUT')
    max_retries: int = Field(3, env='MEDHA_MAX_RETRIES')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)