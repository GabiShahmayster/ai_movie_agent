"""
Configuration settings for the AI Movie Analysis Agent.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ModelConfig:
    """Configuration for the LLM model."""
    name: str = "mistral"
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    timeout: int = 30


@dataclass
class SearchConfig:
    """Configuration for search tools."""
    max_results: int = 10
    timeout: int = 10
    rate_limit_delay: float = 1.0
    cache_ttl: int = 3600  # 1 hour


@dataclass
class AgentConfig:
    """Configuration for the agent behavior."""
    max_iterations: int = 10
    enable_logging: bool = True
    log_level: str = "INFO"
    graph_visualization: bool = True


class Settings:
    """Main application settings."""
    # Environment
    langchain_api_key: Optional[str] = os.getenv("LANGCHAIN_API_KEY")
    langchain_tracing: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_project: str = os.getenv("LANGCHAIN_PROJECT", "AI-Movie-Agent")
    
    # Component configurations
    model: ModelConfig = ModelConfig()
    search: SearchConfig = SearchConfig()
    agent: AgentConfig = AgentConfig()
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if self.langchain_tracing and not self.langchain_api_key:
            raise ValueError("LANGCHAIN_API_KEY is required when tracing is enabled")
        
        if self.model.temperature < 0 or self.model.temperature > 1:
            raise ValueError("Model temperature must be between 0 and 1")
        
        if self.search.max_results <= 0:
            raise ValueError("Search max_results must be positive")


# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the application settings."""
    return settings
