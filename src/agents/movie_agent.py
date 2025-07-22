"""
Movie Analysis Agent implementation using LangGraph.
"""

import logging
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from ..config import get_settings
from ..models import AgentState
from ..tools import get_available_tools

# Set up logging
logger = logging.getLogger(__name__)


class MovieAnalysisAgent:
    """
    AI agent for analyzing movies and tracking actor information.
    """
    
    def __init__(self):
        """Initialize the movie analysis agent."""
        self.settings = get_settings()
        self.tools = get_available_tools()
        self.model = self._create_model()
        self.graph = self._build_graph()
        
        logger.info("MovieAnalysisAgent initialized")
    
    def _create_model(self) -> ChatOllama:
        """Create and configure the language model."""
        model_config = self.settings.model
        
        model = ChatOllama(
            model=model_config.name,
            temperature=model_config.temperature,
            timeout=model_config.timeout
        )
        
        # Bind tools to the model
        model_with_tools = model.bind_tools(self.tools)
        
        logger.info(f"Model created: {model_config.name} with {len(self.tools)} tools")
        return model_with_tools
    
    def _model_node(self, state: AgentState) -> AgentState:
        """
        Process the current state through the language model.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with model response
        """
        try:
            logger.debug("Processing state through model")
            response = self.model.invoke(state["messages"])
            
            logger.debug(f"Model response: {type(response).__name__}")
            return {"messages": response}
            
        except Exception as e:
            logger.error(f"Error in model node: {e}")
            # Return error message to user
            error_msg = "I encountered an error while processing your request. Please try again."
            return {"messages": [HumanMessage(content=error_msg)]}
    
    def _tools_condition(self, state: AgentState) -> str:
        """
        Determine whether to route to tools or end the conversation.
        
        Args:
            state: Current agent state
            
        Returns:
            Next node to execute ("tools" or END)
        """
        try:
            last_message = state["messages"][-1]
            
            # Check if the message contains tool calls
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                logger.debug(f"Routing to tools: {len(last_message.tool_calls)} tool calls")
                return "tools"
            
            # No tool calls, conversation is complete
            logger.debug("Routing to END")
            return END
            
        except Exception as e:
            logger.error(f"Error in tools condition: {e}")
            return END
    
    def _build_graph(self) -> StateGraph:
        """
        Build the agent's execution graph.
        
        Returns:
            Compiled StateGraph for the agent
        """
        logger.info("Building agent graph")
        
        # Initialize the graph
        builder = StateGraph(AgentState)
        
        # Add nodes
        builder.add_node("model", self._model_node)
        builder.add_node("tools", ToolNode(self.tools))
        
        # Add edges
        builder.add_edge(START, "model")
        builder.add_conditional_edges("model", self._tools_condition)
        builder.add_edge("tools", "model")
        
        # Compile the graph
        graph = builder.compile()
        
        # Generate visualization if enabled
        if self.settings.agent.graph_visualization:
            try:
                self._save_graph_visualization(graph)
            except Exception as e:
                logger.warning(f"Could not save graph visualization: {e}")
        
        logger.info("Agent graph built successfully")
        return graph
    
    def _save_graph_visualization(self, graph):
        """Save graph visualization to file."""
        try:
            with open("graph.png", "wb") as f:
                f.write(graph.get_graph().draw_mermaid_png())
            logger.info("Graph visualization saved to graph.png")
        except Exception as e:
            logger.warning(f"Failed to save graph visualization: {e}")
    
    def _create_system_message(self) -> SystemMessage:
        """Create the system message for movie analysis."""
        system_prompt = """You are a movie analysis agent. Your task is to:
        1. Take a movie name from the user
        2. Search for the lead characters/main cast of that movie
        3. Display the lead characters clearly to the user
        4. For each lead actor, find their most recent/latest movies
        5. Present the information in a clear, organized format
        
        Always use the search tool to find accurate, up-to-date information.
        Be thorough in your research and present results clearly.
        
        When presenting results:
        - Start with the movie title and basic information
        - List the main characters and their actors
        - For each actor, show their recent films
        - Use clear formatting and organization
        
        If you encounter errors or cannot find information, explain what went wrong
        and suggest alternatives."""
        
        return SystemMessage(content=system_prompt)
    
    def analyze_movie(self, movie_name: str) -> str:
        """
        Analyze a movie and return the results.
        
        Args:
            movie_name: Name of the movie to analyze
            
        Returns:
            Analysis results as a string
        """
        if not movie_name or not movie_name.strip():
            return "Please provide a valid movie name."
        
        movie_name = movie_name.strip()
        logger.info(f"Starting analysis for movie: {movie_name}")
        
        try:
            # Create the conversation messages
            messages = [
                self._create_system_message(),
                HumanMessage(
                    content=f"Please analyze the movie '{movie_name}'. Find the lead characters and then find the latest movies for each lead actor."
                )
            ]
            
            # Prepare the input state
            input_state = {"messages": messages}
            
            # Run the agent
            logger.debug("Invoking agent graph")
            result = self.graph.invoke(input_state)
            
            # Extract the final response
            final_message = result["messages"][-1]
            response = final_message.content if hasattr(final_message, 'content') else str(final_message)
            
            logger.info(f"Analysis completed for: {movie_name}")
            return response
            
        except Exception as e:
            error_msg = f"Error analyzing movie '{movie_name}': {str(e)}"
            logger.error(error_msg)
            return f"I encountered an error while analyzing '{movie_name}'. Please try again or try a different movie."
    
    def get_agent_info(self) -> dict:
        """Get information about the agent configuration."""
        return {
            "model": self.settings.model.name,
            "temperature": self.settings.model.temperature,
            "tools_count": len(self.tools),
            "tools": [tool.name for tool in self.tools]
        }


def create_agent() -> MovieAnalysisAgent:
    """
    Factory function to create a MovieAnalysisAgent instance.
    
    Returns:
        Configured MovieAnalysisAgent instance
    """
    return MovieAnalysisAgent()
