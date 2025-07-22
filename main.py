"""
Main entry point for the AI Movie Analysis Agent.

Usage:
    python main.py
"""

import sys
import logging
from src import create_agent, get_settings

logger = logging.getLogger(__name__)


def main():
    """Main function to run the movie analysis agent."""
    try:
        # Validate settings
        settings = get_settings()
        settings.validate()
        
        logger.info("Starting AI Movie Analysis Agent")
        logger.info(f"Using model: {settings.model.name}")
        
        # Create the agent
        agent = create_agent()
        
        # Get movie name from user
        print("🎬 AI Movie Analysis Agent")
        print("=" * 40)
        
        movie_name = input("Enter a movie name (or press Enter for 'The Dark Knight'): ").strip()
        
        if not movie_name:
            movie_name = "The Dark Knight"
            print(f"Using default movie: {movie_name}")
        
        print(f"\n🔍 Analyzing movie: {movie_name}")
        print("🤖 AI Agent is working...")
        print("=" * 50)
        
        # Analyze the movie
        result = agent.analyze_movie(movie_name)
        
        # Display results
        print("\n🎭 Movie Analysis Results:")
        print("=" * 50)
        print(result)
        
        # Show agent info
        agent_info = agent.get_agent_info()
        print(f"\n🔧 Agent Info: {agent_info['model']} with {agent_info['tools_count']} tools")
        
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted by user")
        sys.exit(0)
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please check your .env file and settings")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected Error: {e}")
        print("💡 Make sure Ollama is running and the Mistral model is installed!")
        print("   Run: ollama pull mistral")
        sys.exit(1)


if __name__ == "__main__":
    main()
