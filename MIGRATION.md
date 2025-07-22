# Migration Guide: v1.0 → v2.0

## Overview

This guide helps you migrate from the original monolithic structure to the new modular architecture while maintaining all existing functionality.

## Quick Migration (Recommended)

### 1. Backup Your Current Setup
```bash
# Create backups of important files
cp main.py main_v1_backup.py
cp test_movie.py test_movie_v1_backup.py
cp .env .env_v1_backup
cp requirements.txt requirements_v1_backup.txt
```

### 2. Start Using v2.0
```bash
# The enhanced scripts are now the main ones:
python main.py        # Enhanced modular version
python test_movie.py  # Enhanced testing with diagnostics

# Install updated dependencies
pip install -r requirements.txt
```

### 3. Update Configuration
```bash
# Create new .env from template
cp .env.example .env

# Copy your existing settings from .env_v1_backup to .env
# (The new .env has more options but is backward compatible)
```

## Detailed Migration

### File Mapping

| v1.0 Location | v2.0 Location | Notes |
|---------------|---------------|-------|
| `main.py` (old) | `main.py` (new) + `src/agents/movie_agent.py` | Split into modular components |
| `test_movie.py` (old) | `test_movie.py` (new) + `tests/test_agent.py` | Enhanced testing with unit tests |
| Direct imports | `src/` package structure | Organized into logical modules |
| Hardcoded settings | `src/config/settings.py` | Centralized configuration |
| Basic error handling | Enhanced throughout `src/` | Comprehensive error management |

### Code Migration Examples

#### Agent Usage
```python
# v1.0 - Direct graph usage
from main import graph
result = graph.invoke({"messages": messages})

# v2.0 - Agent class
from src import create_agent
agent = create_agent()
result = agent.analyze_movie("Movie Name")
```

#### Tools Usage
```python
# v1.0 - Direct tool imports
from main import search_movie_info, calculator

# v2.0 - Modular tools
from src.tools import search_movie_info, calculator, get_available_tools
tools = get_available_tools()
```

#### Configuration
```python
# v1.0 - Hardcoded values
model = ChatOllama(model="mistral", temperature=0.1)

# v2.0 - Configurable
from src.config import get_settings
settings = get_settings()
model = ChatOllama(
    model=settings.model.name,
    temperature=settings.model.temperature
)
```

### Custom Code Migration

If you have custom code that imports from the old structure:

#### 1. Update Imports
```python
# Old imports
from main import graph, model, tools_condition, model_node

# New imports
from src.agents import create_agent
from src.models import AgentState
from src.tools import get_available_tools
```

#### 2. Adapt to New Agent Class
```python
# Old direct usage
messages = [SystemMessage(...), HumanMessage(...)]
result = graph.invoke({"messages": messages})

# New agent usage
agent = create_agent()
result = agent.analyze_movie("Movie Name")

# Or for custom usage
from src.agents.movie_agent import MovieAnalysisAgent
agent = MovieAnalysisAgent()
# Access internal components: agent.graph, agent.model, etc.
```

#### 3. Configuration Updates
```python
# Old hardcoded approach
search = DuckDuckGoSearchRun()

# New configurable approach
from src.tools.search_tools import get_search_instance, perform_search
search = get_search_instance()
# Or use the enhanced wrapper
result = perform_search("query")  # Includes caching, error handling
```

## New Features Available

### 1. Enhanced Error Handling
```python
from src.tools import perform_search
result = perform_search("movie query")
if result.success:
    print(result.results)
else:
    print(f"Search failed: {result.error}")
```

### 2. Caching System
```python
# Automatic caching with TTL
from src.tools import clear_search_cache
clear_search_cache()  # Clear when needed
```

### 3. Comprehensive Logging
```python
import logging
logger = logging.getLogger('src.agents.movie_agent')
logger.setLevel(logging.DEBUG)  # See detailed operations
```

### 4. Configuration Management
```python
from src.config import get_settings
settings = get_settings()
settings.model.temperature = 0.2
settings.search.cache_ttl = 7200
settings.validate()
```

### 5. Testing Infrastructure
```bash
# Run comprehensive tests
python tests/test_agent.py

# Run diagnostics
python test_movie_new.py diagnostic
```

## Gradual Migration Path

### Phase 1: Side-by-Side (Week 1)
- Keep using `main.py` for production
- Test `main_new.py` in parallel
- Compare outputs for consistency

### Phase 2: Feature Testing (Week 2)
- Use new testing tools: `python test_movie_new.py diagnostic`
- Test enhanced error handling
- Verify caching behavior

### Phase 3: Full Migration (Week 3)
- Switch to `main_new.py` as primary
- Update any custom integrations
- Remove old files (keep backups)

## Compatibility Notes

### What's Compatible
- ✅ All existing functionality preserved
- ✅ Same model and tools behavior
- ✅ Environment variables (with new optional ones)
- ✅ Input/output formats unchanged

### What's Enhanced
- 🚀 Better error messages and recovery
- 🚀 Configurable settings
- 🚀 Caching for improved performance
- 🚀 Comprehensive logging
- 🚀 Input sanitization and security
- 🚀 Modular architecture for extensions

### Breaking Changes
- ⚠️ Import paths changed (if you have custom code)
- ⚠️ Direct graph access requires agent instance
- ⚠️ Some internal function signatures changed

## Rollback Plan

If you need to rollback to v1.0:

```bash
# Restore backups
cp main_v1_backup.py main.py
cp test_movie_v1_backup.py test_movie.py
cp .env_v1_backup .env
cp requirements_v1_backup.txt requirements.txt

# Reinstall old dependencies
pip install -r requirements.txt

# Use original commands
python main.py
python test_movie.py
```

## Troubleshooting Migration Issues

### Import Errors
```bash
# Solution 1: Install in development mode
pip install -e .

# Solution 2: Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Module Not Found
```python
# Make sure you're using new import paths
from src import create_agent  # Not from main import
```

### Configuration Errors
```bash
# Run diagnostics to identify issues
python test_movie_new.py diagnostic

# Check your .env file format
python test_movie_new.py config
```

## Getting Help

1. **Run diagnostics first**: `python test_movie_new.py diagnostic`
2. **Check the logs**: Enable debug logging in .env
3. **Compare with v1.0**: Run both versions side-by-side
4. **Review the examples**: See README_new.md for usage patterns

## Benefits of Migration

- **🛡️ Security**: Input sanitization and secure configuration
- **🏗️ Maintainability**: Modular architecture easier to extend
- **🔍 Debugging**: Comprehensive logging and error handling
- **⚡ Performance**: Caching and rate limiting
- **🧪 Testing**: Full test suite for reliability
- **📈 Future-proof**: Ready for web API, database, and UI extensions

The migration provides immediate benefits while maintaining full compatibility with your existing workflows.
