"""
Search tools for the AI Movie Analysis Agent.
"""

import logging
import time
import ast
from functools import lru_cache
from typing import Optional
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

from ..config import get_settings
from ..models import SearchResult

# Set up logging
logger = logging.getLogger(__name__)

# Global search instance
_search_instance: Optional[DuckDuckGoSearchRun] = None


def get_search_instance() -> DuckDuckGoSearchRun:
    """Get or create the search instance."""
    global _search_instance
    if _search_instance is None:
        _search_instance = DuckDuckGoSearchRun()
    return _search_instance


def sanitize_query(query: str) -> str:
    """Sanitize search query to prevent injection attacks."""
    if not query or not isinstance(query, str):
        return ""
    
    # Remove potentially dangerous characters
    import re
    sanitized = re.sub(r'[<>"\';]', '', query.strip())
    
    # Limit length
    max_length = 200
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        logger.warning(f"Query truncated to {max_length} characters")
    
    return sanitized


@lru_cache(maxsize=100)
def _cached_search(query: str, cache_key: int) -> SearchResult:
    """
    Internal cached search function.
    Cache key changes based on time to implement TTL.
    """
    settings = get_settings()
    search = get_search_instance()
    
    try:
        # Add rate limiting
        time.sleep(settings.search.rate_limit_delay)
        
        logger.info(f"Performing search: {query}")
        result = search.run(query)
        
        logger.debug(f"Search successful for: {query}")
        return SearchResult(query=query, results=result, success=True)
        
    except ConnectionError as e:
        error_msg = "Network connection error. Please check your internet connection."
        logger.error(f"Connection error for query '{query}': {e}")
        return SearchResult(query=query, results="", success=False, error=error_msg)
        
    except TimeoutError as e:
        error_msg = "Search request timed out. Please try again later."
        logger.error(f"Timeout error for query '{query}': {e}")
        return SearchResult(query=query, results="", success=False, error=error_msg)
        
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        logger.error(f"Unexpected error for query '{query}': {e}")
        return SearchResult(query=query, results="", success=False, error=error_msg)


def perform_search(query: str) -> SearchResult:
    """
    Perform a web search with caching and error handling.
    
    Args:
        query: The search query string
        
    Returns:
        SearchResult object containing the results or error information
    """
    sanitized_query = sanitize_query(query)
    if not sanitized_query:
        return SearchResult(
            query=query, 
            results="", 
            success=False, 
            error="Invalid or empty search query"
        )
    
    # Generate cache key based on current time for TTL
    settings = get_settings()
    cache_key = int(time.time() // settings.search.cache_ttl)
    
    return _cached_search(sanitized_query, cache_key)


@tool
def search_movie_info(query: str) -> str:
    """
    Search for movie information including cast, characters, and actor details.
    Use this to find lead characters in movies and their latest films.
    
    Args:
        query: Search query for movie information
        
    Returns:
        Search results as a string
    """
    result = perform_search(query)
    return str(result)


@tool
def calculator(expression: str) -> str:
    """
    Calculate the result of a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Result of the calculation as a string
    """
    try:
        # Sanitize the expression
        if not expression or not isinstance(expression, str):
            return "Error: Invalid expression"
        
        # Remove potentially dangerous characters
        import re
        sanitized = re.sub(r'[^0-9+\-*/().\s]', '', expression.strip())
        
        if not sanitized:
            return "Error: Empty expression after sanitization"
        
        logger.info(f"Calculating: {sanitized}")
        result = ast.literal_eval(sanitized)
        
        logger.debug(f"Calculation result: {result}")
        return str(result)
        
    except (ValueError, SyntaxError) as e:
        error_msg = f"Invalid mathematical expression: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
        
    except ZeroDivisionError:
        error_msg = "Division by zero"
        logger.error(error_msg)
        return f"Error: {error_msg}"
        
    except Exception as e:
        error_msg = f"Calculation error: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


def get_available_tools():
    """Get list of available tools."""
    return [search_movie_info, calculator]


def clear_search_cache():
    """Clear the search cache."""
    _cached_search.cache_clear()
    logger.info("Search cache cleared")
