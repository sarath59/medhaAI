from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
class MedhaConfig(BaseSettings):
    openai_api_key: Optional[str] = Field(None, env='OPENAI_API_KEY')
    anthropic_api_key: Optional[str] = Field(None, env='ANTHROPIC_API_KEY')
    default_llm: str = Field('openai', env='MEDHA_DEFAULT_LLM')
    default_model: str = Field('gpt-3.5-turbo', env='MEDHA_DEFAULT_MODEL')
    max_tokens: int = Field(500, env='MEDHA_MAX_TOKENS')
    temperature: float = Field(0.7, env='MEDHA_TEMPERATURE')
    memory_type: str = Field('in_memory', env='MEDHA_MEMORY_TYPE')
    memory_capacity: int = Field(1000, env='MEDHA_MEMORY_CAPACITY')
    db_url: Optional[str] = Field(None, env='MEDHA_DB_URL')
    planning_max_depth: int = Field(3, env='MEDHA_PLANNING_MAX_DEPTH')
    execution_max_concurrent: int = Field(5, env='MEDHA_EXECUTION_MAX_CONCURRENT')
    log_level: str = Field('INFO', env='MEDHA_LOG_LEVEL')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'