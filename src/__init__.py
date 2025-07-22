"""
AI Movie Analysis Agent - Source Package

A modular, production-ready movie analysis agent using LangGraph.
"""

import logging
from .config import get_settings
from .agents import create_agent
from .models import MovieAnalysisResult
from .tools import get_available_tools

# Set up logging
def setup_logging():
    """Set up application logging."""
    settings = get_settings()
    
    if settings.agent.enable_logging:
        level = getattr(logging, settings.agent.log_level.upper(), logging.INFO)
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set specific loggers
        logging.getLogger('langchain').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)


# Initialize logging when package is imported
setup_logging()

__version__ = "0.2.0"
__all__ = [
    "get_settings",
    "create_agent", 
    "MovieAnalysisResult",
    "get_available_tools",
    "setup_logging"
]
