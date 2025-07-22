#https://medium.com/data-science-collective/build-smarter-ai-agents-for-free-using-langgraph-ollama-9096ad7952aa

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
import ast
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# Instantiate the search tool
search = DuckDuckGoSearchRun()

class State(TypedDict):
    messages: Annotated[list, add_messages]

def tools_condition(state: State) -> str:
    """
    Route to tools node when a tool call is detected in the last message,
    otherwise mark as complete.
    """
    last_message = state["messages"][-1]
    # Check if the message contains tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # No tool calls, so we're done
    return END

# Build the model node
def model_node(state: State) -> State:
    # Run the model
    res = model.invoke(state["messages"])
    # Return the content of the message.
    return {"messages": res}

# Create a calculator function (keeping for potential future use)
@tool
def calculator(query: str) -> str:
    """Use this tool to calculate the result of a mathematical expression."""
    return str(ast.literal_eval(query))

@tool
def search_movie_info(query: str) -> str:
    """
    Search for movie information including cast, characters, and actor details.
    Use this to find lead characters in movies and their latest films.
    """
    try:
        result = search.run(query)
        return result
    except Exception as e:
        return f"Search error: {str(e)}"

if __name__ == "__main__":
    # Define tools - focusing on movie search
    tools = [search_movie_info, calculator]
    
    # Create model with system prompt for movie analysis
    model = ChatOllama(
        model="mistral", 
        temperature=0.1
    ).bind_tools(tools)

    # Initialize the graph
    builder = StateGraph(State)

    # Build the nodes
    builder.add_node("model", model_node)
    builder.add_node("tools", ToolNode(tools))

    # Add the edges
    builder.add_edge(START, "model")
    builder.add_conditional_edges("model", tools_condition)
    builder.add_edge("tools", "model")

    # Compile the graph
    graph = builder.compile()
    with open("graph.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())

    from langchain_core.messages import HumanMessage, SystemMessage

    # Get movie name from user
    movie_name = input("🎬 Enter a movie name: ")
    
    if not movie_name:
        movie_name = "The Dark Knight"  # Default movie
        print(f"Using default movie: {movie_name}")

    # Create the conversation with system instructions and user input
    messages = [
        SystemMessage(
            content="""You are a movie analysis agent. Your task is to:
            1. Take a movie name from the user
            2. Search for the lead characters/main cast of that movie
            3. Display the lead characters clearly to the user
            4. For each lead actor, find their most recent/latest movies
            5. Present the information in a clear, organized format
            
            Always use the search tool to find accurate, up-to-date information.
            Be thorough in your research and present results clearly."""
        ),
        HumanMessage(
            content=f"Please analyze the movie '{movie_name}'. Find the lead characters and then find the latest movies for each lead actor."
        )
    ]

    input_data = {"messages": messages}

    print(f"\n🔍 Analyzing movie: {movie_name}")
    print("=" * 50)

    try:
        result = graph.invoke(input_data)
        print("\n🎭 Movie Analysis Results:")
        print("=" * 50)
        print(result["messages"][-1].content)
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
