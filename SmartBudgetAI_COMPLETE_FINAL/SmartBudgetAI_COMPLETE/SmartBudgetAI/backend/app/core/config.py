from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Smart Budget AI"
    environment: str = "development"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./smart_budget.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    llm_provider: str = "local"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    vector_provider: str = "local"
    pinecone_api_key: str = ""
    pinecone_index: str = "smart-budget-ai"
    pinecone_namespace: str = "default"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
