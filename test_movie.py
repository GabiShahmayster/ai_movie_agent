"""
Interactive test script for the AI Movie Analysis Agent.
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src import create_agent, get_settings

# Set up logging for interactive testing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_movie_analysis():
    """Interactive test of the AI agent's movie analysis functionality."""
    
    # Sample movies for testing
    sample_movies = [
        "The Dark Knight",
        "Inception", 
        "Titanic",
        "The Avengers",
        "Pulp Fiction",
        "Interstellar",
        "The Matrix",
        "Forrest Gump"
    ]
    
    print("🎬 AI Movie Analysis Agent - Interactive Test")
    print("=" * 50)
    print("Sample movies you can try:")
    for i, movie in enumerate(sample_movies, 1):
        print(f"  {i}. {movie}")
    
    try:
        # Validate configuration
        settings = get_settings()
        settings.validate()
        
        # Create agent
        print("\n🤖 Initializing AI Agent...")
        agent = create_agent()
        
        # Show agent info
        agent_info = agent.get_agent_info()
        print(f"✅ Agent ready! Using {agent_info['model']} with {agent_info['tools_count']} tools")
        
        while True:
            print("\n" + "=" * 50)
            movie_name = input("🎭 Enter a movie name (or 'quit' to exit): ").strip()
            
            if movie_name.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for testing! Goodbye!")
                break
                
            if not movie_name:
                movie_name = "Inception"
                print(f"Using default movie: {movie_name}")
            
            print(f"\n🔍 Analyzing: {movie_name}")
            print("🤖 AI Agent is working... (this may take a moment)")
            print("-" * 50)
            
            try:
                # Analyze the movie
                result = agent.analyze_movie(movie_name)
                
                # Display results
                print("\n🎭 Analysis Results:")
                print("=" * 50)
                print(result)
                
                # Ask if user wants to continue
                print("\n" + "=" * 50)
                continue_test = input("🔄 Analyze another movie? (y/n): ").strip().lower()
                
                if continue_test in ['n', 'no']:
                    print("👋 Thanks for testing! Goodbye!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⏸️  Analysis interrupted by user")
                continue_choice = input("Continue with another movie? (y/n): ").strip().lower()
                if continue_choice in ['n', 'no']:
                    break
                    
            except Exception as e:
                logger.error(f"Error during analysis: {e}")
                print(f"\n❌ Error: {e}")
                print("💡 Make sure Ollama is running and the Mistral model is installed!")
                
                continue_choice = input("Try another movie? (y/n): ").strip().lower()
                if continue_choice in ['n', 'no']:
                    break
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please check your .env file and settings")
        return False
        
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        print(f"\n❌ Failed to initialize agent: {e}")
        print("💡 Troubleshooting tips:")
        print("   1. Make sure Ollama is running: ollama serve")
        print("   2. Install Mistral model: ollama pull mistral")
        print("   3. Check your internet connection for search functionality")
        return False
    
    return True


def test_configuration():
    """Test the configuration system."""
    print("\n🔧 Testing Configuration...")
    
    try:
        settings = get_settings()
        print(f"✅ Model: {settings.model.name}")
        print(f"✅ Temperature: {settings.model.temperature}")
        print(f"✅ Search timeout: {settings.search.timeout}s")
        print(f"✅ Logging: {'enabled' if settings.agent.enable_logging else 'disabled'}")
        
        settings.validate()
        print("✅ Configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_tools():
    """Test the tools functionality."""
    print("\n🔨 Testing Tools...")
    
    try:
        from src.tools import get_available_tools, perform_search
        
        tools = get_available_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # Test search function
        print("\n🔍 Testing search function...")
        test_result = perform_search("test query")
        print(f"✅ Search function working: {test_result.success}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tools error: {e}")
        return False


def run_diagnostic():
    """Run full diagnostic test."""
    print("🩺 Running Full Diagnostic...")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Tools", test_tools),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results[test_name] = False
    
    print("\n📊 Diagnostic Results:")
    print("=" * 30)
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print(f"\nOverall: {'✅ All tests passed' if all_passed else '❌ Some tests failed'}")
    
    return all_passed


def main():
    """Main function for interactive testing."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "diagnostic":
            success = run_diagnostic()
            sys.exit(0 if success else 1)
        elif command == "config":
            success = test_configuration()
            sys.exit(0 if success else 1)
        elif command == "tools":
            success = test_tools()
            sys.exit(0 if success else 1)
        else:
            print("Available commands: diagnostic, config, tools")
            print("Or run without arguments for interactive movie testing")
            sys.exit(1)
    else:
        # Interactive movie analysis testing
        success = test_movie_analysis()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
