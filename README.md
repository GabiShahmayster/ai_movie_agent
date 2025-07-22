# AI Movie Analysis Agent v2.0 🎬

A **production-ready**, modular AI agent that analyzes movies, finds lead characters, and tracks actors' latest films using LangGraph, Ollama, and DuckDuckGo search.

## ✨ New in v2.0

- **🏗️ Modular Architecture**: Clean separation of concerns
- **🔒 Enhanced Security**: Input sanitization and secure configuration  
- **📊 Comprehensive Logging**: Full observability and debugging
- **🧪 Complete Testing**: Unit tests and integration tests
- **⚡ Performance**: Caching and rate limiting
- **🛠️ Production Ready**: Error handling and configuration management

## 🚀 Features

- **Movie Character Analysis**: Identifies lead characters and main cast
- **Actor Tracking**: Discovers latest movies for each lead actor
- **Web Search Integration**: Uses DuckDuckGo for current information
- **Interactive Interface**: Enhanced command-line experience
- **Conversational Flow**: LangGraph-based state management
- **Local LLM**: Uses Ollama with Mistral for privacy
- **Caching System**: Reduces API calls and improves performance
- **Error Recovery**: Robust error handling and user feedback

## 📁 Project Structure

```
ai_agent/
├── src/                      # Source code (NEW!)
│   ├── agents/              # Agent implementations
│   │   └── movie_agent.py   # Main MovieAnalysisAgent
│   ├── tools/               # Search and utility tools
│   │   └── search_tools.py  # Enhanced search with caching
│   ├── models/              # Data models and state
│   │   └── state_models.py  # Type definitions
│   └── config/              # Configuration management
│       └── settings.py      # Centralized settings
├── tests/                   # Test suite (NEW!)
│   └── test_agent.py       # Comprehensive tests
├── main.py                 # Enhanced modular main script
├── test_movie.py           # Enhanced interactive testing
├── .env.example            # Secure environment template
├── requirements.txt        # Updated dependencies
└── pyproject.toml          # Modern Python packaging
```

## 🔧 Installation

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai/) installed locally
- Mistral model: `ollama pull mistral`

### Setup

1. **Clone and navigate**:
```bash
cd ai_agent
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
# Basic installation
pip install -r requirements.txt

# Or with development tools
pip install -e ".[dev]"
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings (API keys are optional)
```

## 🎯 Usage

### Quick Start

```bash
# Run the enhanced agent
python main.py

# Interactive testing with diagnostics
python test_movie.py

# Run diagnostics only
python test_movie.py diagnostic
```

### Advanced Usage

```python
from src import create_agent

# Create and use the agent
agent = create_agent()
result = agent.analyze_movie("Inception")
print(result)

# Get agent information
info = agent.get_agent_info()
print(f"Using {info['model']} with {info['tools_count']} tools")
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python tests/test_agent.py config     # Configuration tests
python tests/test_agent.py tools     # Tools tests  
python tests/test_agent.py agent     # Agent tests

# Run with coverage
python -m pytest tests/ --cov=src
```

### Interactive Testing

```bash
# Full interactive test
python test_movie.py

# Component diagnostics
python test_movie.py diagnostic
python test_movie.py config
python test_movie.py tools
```

## ⚙️ Configuration

### Environment Variables

Create `.env` from `.env.example`:

```env
# Optional LangChain tracing
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=AI-Movie-Agent

# Model settings (optional - defaults used if not set)
MODEL_NAME=mistral
MODEL_TEMPERATURE=0.1

# Search configuration
SEARCH_CACHE_TTL=3600
SEARCH_RATE_LIMIT_DELAY=1.0

# Logging
AGENT_LOG_LEVEL=INFO
AGENT_ENABLE_LOGGING=true
```

### Programmatic Configuration

```python
from src.config import get_settings

settings = get_settings()
settings.model.temperature = 0.2
settings.search.cache_ttl = 7200
settings.validate()  # Validate settings
```

## 🔒 Security Features

- **Input Sanitization**: Prevents injection attacks
- **Environment Variables**: Secure configuration management
- **Rate Limiting**: Prevents API abuse
- **Error Handling**: No sensitive data in error messages
- **Caching**: Reduces external API calls

## 📊 Performance Features

- **LRU Caching**: Search results cached with TTL
- **Rate Limiting**: Configurable delays between API calls
- **Connection Pooling**: Reused search instances
- **Lazy Loading**: Components loaded on demand

## 🔍 Debugging

### Logging

```python
import logging

# Enable debug logging
logging.getLogger('src').setLevel(logging.DEBUG)

# View agent operations
logger = logging.getLogger('src.agents.movie_agent')
```

### Diagnostics

```bash
# Check system health
python test_movie.py diagnostic

# Test individual components
python test_movie.py config
python test_movie.py tools
```

## 🚀 Migration from v1.0

### Quick Migration

1. **Backup your current setup**:
```bash
cp main.py main_v1_backup.py
cp test_movie.py test_movie_v1_backup.py
```

2. **Use the current scripts**:
```bash
# Enhanced version now available as:
python main.py

# Enhanced testing now available as:
python test_movie.py
```

3. **Update your .env**:
```bash
cp .env .env.backup
cp .env.example .env
# Copy your settings from .env.backup to .env
```

### Code Migration

If you have custom code using the old structure:

```python
# Old way
from main import graph, model

# New way  
from src import create_agent
agent = create_agent()
# Use agent.graph and agent.model
```

## 🤝 Contributing

### Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run code formatting
black src/ tests/

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Run full test suite
pytest tests/ --cov=src
```

### Code Standards

- **Black** for formatting
- **Flake8** for linting  
- **MyPy** for type checking
- **Pytest** for testing
- Minimum 80% test coverage

## 📈 Roadmap

### Upcoming Features

- **🌐 Web API**: FastAPI-based REST API
- **💾 Database**: Persistent storage for analyses
- **🎨 Web UI**: React-based frontend
- **📊 Analytics**: Usage metrics and insights
- **🔄 Async**: Asynchronous processing
- **📱 Mobile**: Mobile app support

### Installation Commands

```bash
# Future web API
pip install -e ".[web]"

# Future database support  
pip install -e ".[db]"

# Future caching with Redis
pip install -e ".[cache]"

# Everything
pip install -e ".[all]"
```

## 🆘 Troubleshooting

### Common Issues

**Ollama Connection Error**:
```bash
# Start Ollama service
ollama serve

# Verify Mistral model
ollama list
ollama pull mistral  # If not installed
```

**Import Errors**:
```bash
# Install in development mode
pip install -e .

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Search Failures**:
- Check internet connection
- Verify DuckDuckGo accessibility
- Review rate limiting settings

### Get Help

1. **Run diagnostics**: `python test_movie.py diagnostic`
2. **Check logs**: Enable debug logging in your .env file
3. **Review configuration**: Ensure all settings are valid
4. **Test components**: Run individual component tests

## 📝 Example Output

```
🎬 AI Movie Analysis Agent
==========================================

Enter a movie name (or press Enter for 'The Dark Knight'): Inception

🔍 Analyzing movie: Inception
🤖 AI Agent is working...
==================================================

🎭 Movie Analysis Results:
==================================================

**INCEPTION (2010) - Analysis Complete**

**Lead Characters & Cast:**
• Dom Cobb - Leonardo DiCaprio
• Arthur - Tom Hardy  
• Ariadne - Marion Cotillard
• Eames - Tom Hardy
• Saito - Ken Watanabe

**Latest Films by Lead Actors:**

**Leonardo DiCaprio:**
- Don't Look Up (2021)
- Once Upon a Time in Hollywood (2019)
- The Revenant (2015)

**Tom Hardy:**
- Venom: Let There Be Carnage (2021)
- Capone (2020)
- 1917 (2019)

**Marion Cotillard:**
- Annette (2021)
- Allied (2016)
- Macbeth (2015)

🔧 Agent Info: mistral with 2 tools
```

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain/LangGraph**: For the agent framework
- **Ollama**: For local LLM inference
- **DuckDuckGo**: For search capabilities
- **Python Community**: For the excellent ecosystem

---

**Ready to analyze some movies? 🍿**

```bash
python main.py
```
