#https://medium.com/data-science-collective/build-smarter-ai-agents-for-free-using-langgraph-ollama-9096ad7952aa

from langchain_core.tools import tool
import ast
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

# Instantiate the object.
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

# Create a calculator function
@tool
def calculator(query: str) -> str:
  # Explain the aim of this function
  """Use this tool to calculate the result of a mathematical expression."""
  # Use literal_eval to safely evaluate mathematical expressions provided in string format.
  return ast.literal_eval(query)

if __name__ == "__main__":
    # Define a variable to hold all the tools we'll use
    # tools = [search, calculator]
    search = DuckDuckGoSearchRun()
    tools = [search]
    model = ChatOllama(model="mistral", temperature=0.1).bind_tools(tools)

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

    from langchain_core.messages import HumanMessage

    # Create an input
    input = {
        "messages": [
            HumanMessage(
                "What is the radius of the earth?"
            )
        ]
    }

    result = graph.invoke(input)
    print(result)
    print("--------------The AI Agent's Answer------------------")
    print(result["messages"][-1].content)