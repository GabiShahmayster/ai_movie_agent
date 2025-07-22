# AI Movie Analysis Agent with LangGraph

A conversational AI agent that analyzes movies, finds lead characters, and tracks actors' latest films using LangGraph, Ollama, and DuckDuckGo search.

## Features

- **Movie Character Analysis**: Finds lead characters/main cast of any movie
- **Actor Tracking**: Discovers the latest movies for each lead actor
- **Web Search Integration**: Uses DuckDuckGo for current movie and actor information
- **Interactive Interface**: Command-line interface for movie analysis
- **Conversational Flow**: LangGraph-based state management for natural conversations
- **Local LLM**: Uses Ollama with Mistral model for privacy-focused AI

## How It Works

1. **Input**: You provide a movie name
2. **Character Search**: Agent searches for the lead characters/cast
3. **Display Cast**: Shows you the main actors and their characters
4. **Latest Films**: For each actor, finds their most recent movies
5. **Results**: Presents everything in an organized format

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

### Basic Usage
Run the main script:
```bash
python main.py
```
Enter a movie name when prompted, and the agent will analyze it completely.

### Test Script
Run the interactive test:
```bash
python test_movie.py
```
This provides sample movies and interactive testing.

### Example Analysis

**Input**: "The Dark Knight"

**Output**:
- Lead Characters: Bruce Wayne/Batman, Joker, Harvey Dent, etc.
- Lead Actors: Christian Bale, Heath Ledger, Aaron Eckhart
- Latest Films: Recent movies for each actor

## Project Structure

```
ai_agent/
├── main.py              # Main movie analysis agent
├── test_movie.py        # Interactive testing script
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
├── langgraph.json      # LangGraph configuration
├── README.md           # This file
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
└── .venv/              # Virtual environment (not tracked)
```

## Sample Movies to Try

- The Dark Knight
- Inception
- Titanic  
- The Avengers
- Pulp Fiction
- Interstellar
- The Matrix
- Forrest Gump

## Customization

### Adding New Tools

To extend the agent's capabilities, add new tools to `main.py`:

```python
@tool
def your_custom_tool(query: str) -> str:
    """Description of your tool"""
    # Your implementation here
    return result

tools = [search_movie_info, calculator, your_custom_tool]
```

### Modifying Search Behavior

The `search_movie_info` tool can be customized to focus on specific types of movie information or use different search strategies.

## Troubleshooting

- **Ollama not found**: Make sure Ollama is installed and running
- **Mistral model missing**: Run `ollama pull mistral`
- **Search failures**: Check your internet connection
- **No results**: Try more popular/recent movies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various movies
5. Submit a pull request

## License

MIT License - see LICENSE file for details
