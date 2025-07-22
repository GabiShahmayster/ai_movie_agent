"""
State models for the AI Movie Analysis Agent.
"""

from typing import TypedDict, Annotated, List, Optional
from dataclasses import dataclass
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State for the movie analysis agent."""
    messages: Annotated[list, add_messages]


@dataclass
class MovieInfo:
    """Information about a movie."""
    title: str
    year: Optional[int] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    plot: Optional[str] = None


@dataclass
class Character:
    """Information about a movie character."""
    name: str
    actor: str
    description: Optional[str] = None


@dataclass
class Actor:
    """Information about an actor."""
    name: str
    latest_movies: List[str] = None
    birth_year: Optional[int] = None
    
    def __post_init__(self):
        if self.latest_movies is None:
            self.latest_movies = []


@dataclass
class MovieAnalysisResult:
    """Complete movie analysis result."""
    movie: MovieInfo
    characters: List[Character] = None
    actors: List[Actor] = None
    analysis_summary: Optional[str] = None
    
    def __post_init__(self):
        if self.characters is None:
            self.characters = []
        if self.actors is None:
            self.actors = []


class SearchResult:
    """Wrapper for search results."""
    
    def __init__(self, query: str, results: str, success: bool = True, error: Optional[str] = None):
        self.query = query
        self.results = results
        self.success = success
        self.error = error
        
    def __str__(self) -> str:
        if self.success:
            return self.results
        return f"Search failed: {self.error}"
