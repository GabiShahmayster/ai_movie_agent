# AI Agent with LangGraph

A conversational AI agent built with LangGraph, Ollama, and DuckDuckGo search capabilities.

## Features

- **Web Search**: Uses DuckDuckGo to find current information
- **Mathematical Calculations**: Built-in calculator tool for math expressions
- **Conversational Flow**: LangGraph-based state management for natural conversations
- **Local LLM**: Uses Ollama with Mistral model for privacy-focused AI

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai/) installed locally
- Mistral model downloaded in Ollama (`ollama pull mistral`)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai_agent
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the agent:
```bash
python main.py
```

The agent will answer the predefined question "What is the radius of the earth?" using web search.

## Project Structure

```
ai_agent/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── .venv/              # Virtual environment (not tracked)
```

## How It Works

1. **State Management**: Uses TypedDict to manage conversation state
2. **Tool Routing**: Conditionally routes to tools based on LLM output
3. **Web Search**: Automatically searches DuckDuckGo when needed
4. **Calculator**: Evaluates mathematical expressions safely

## Customization

To add new tools, extend the `tools` list in `main.py`:

```python
@tool
def your_custom_tool(input: str) -> str:
    """Description of your tool"""
    # Your implementation here
    return result

tools = [search, calculator, your_custom_tool]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details
