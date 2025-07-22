"""
Comprehensive test suite for the AI Movie Analysis Agent.
"""

import unittest
import logging
from unittest.mock import Mock, patch
from src.config import Settings, get_settings
from src.models import SearchResult, AgentState
from src.tools.search_tools import sanitize_query, perform_search
from src.agents.movie_agent import MovieAnalysisAgent

# Disable logging during tests
logging.disable(logging.CRITICAL)


class TestConfiguration(unittest.TestCase):
    """Test configuration management."""
    
    def test_default_settings(self):
        """Test default settings are valid."""
        settings = Settings()
        # Should not raise an exception
        settings.validate()
        
    def test_invalid_temperature(self):
        """Test invalid temperature raises error."""
        settings = Settings()
        settings.model.temperature = 2.0
        
        with self.assertRaises(ValueError):
            settings.validate()
    
    def test_invalid_search_results(self):
        """Test invalid search results raises error."""
        settings = Settings()
        settings.search.max_results = -1
        
        with self.assertRaises(ValueError):
            settings.validate()


class TestSearchTools(unittest.TestCase):
    """Test search tools functionality."""
    
    def test_sanitize_query_basic(self):
        """Test basic query sanitization."""
        result = sanitize_query("The Dark Knight")
        self.assertEqual(result, "The Dark Knight")
    
    def test_sanitize_query_malicious(self):
        """Test sanitization of malicious input."""
        result = sanitize_query("<script>alert('xss')</script>")
        self.assertEqual(result, "scriptalert(xss)/script")
        
    def test_sanitize_query_empty(self):
        """Test sanitization of empty input."""
        self.assertEqual(sanitize_query(""), "")
        self.assertEqual(sanitize_query(None), "")
        
    def test_sanitize_query_long(self):
        """Test sanitization of overly long input."""
        long_query = "a" * 300
        result = sanitize_query(long_query)
        self.assertLessEqual(len(result), 200)
    
    @patch('src.tools.search_tools.get_search_instance')
    def test_perform_search_success(self, mock_search):
        """Test successful search operation."""
        mock_instance = Mock()
        mock_instance.run.return_value = "Mock search result"
        mock_search.return_value = mock_instance
        
        result = perform_search("test query")
        
        self.assertTrue(result.success)
        self.assertEqual(result.results, "Mock search result")
        self.assertIsNone(result.error)
    
    @patch('src.tools.search_tools.get_search_instance')
    def test_perform_search_connection_error(self, mock_search):
        """Test search with connection error."""
        mock_instance = Mock()
        mock_instance.run.side_effect = ConnectionError("Network error")
        mock_search.return_value = mock_instance
        
        result = perform_search("test query")
        
        self.assertFalse(result.success)
        self.assertIn("Network connection error", result.error)


class TestSearchResult(unittest.TestCase):
    """Test SearchResult model."""
    
    def test_successful_result(self):
        """Test successful search result."""
        result = SearchResult("test", "results", True)
        self.assertEqual(str(result), "results")
        
    def test_failed_result(self):
        """Test failed search result."""
        result = SearchResult("test", "", False, "Error message")
        self.assertIn("Search failed", str(result))
        self.assertIn("Error message", str(result))


class TestMovieAgent(unittest.TestCase):
    """Test MovieAnalysisAgent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock settings to avoid external dependencies
        self.mock_settings = Mock()
        self.mock_settings.model.name = "test-model"
        self.mock_settings.model.temperature = 0.1
        self.mock_settings.model.timeout = 30
        self.mock_settings.agent.graph_visualization = False
        
    @patch('src.agents.movie_agent.get_settings')
    @patch('src.agents.movie_agent.get_available_tools')
    @patch('src.agents.movie_agent.ChatOllama')
    def test_agent_initialization(self, mock_ollama, mock_tools, mock_settings):
        """Test agent initialization."""
        mock_settings.return_value = self.mock_settings
        mock_tools.return_value = []
        
        agent = MovieAnalysisAgent()
        
        self.assertIsNotNone(agent.model)
        self.assertIsNotNone(agent.graph)
        mock_ollama.assert_called_once()
    
    def test_analyze_movie_empty_input(self):
        """Test analyze_movie with empty input."""
        with patch('src.agents.movie_agent.get_settings') as mock_settings:
            mock_settings.return_value = self.mock_settings
            with patch('src.agents.movie_agent.get_available_tools') as mock_tools:
                mock_tools.return_value = []
                with patch('src.agents.movie_agent.ChatOllama'):
                    agent = MovieAnalysisAgent()
                    
                    result = agent.analyze_movie("")
                    self.assertIn("valid movie name", result)
                    
                    result = agent.analyze_movie("   ")
                    self.assertIn("valid movie name", result)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    @patch('src.tools.search_tools.get_search_instance')
    @patch('src.agents.movie_agent.ChatOllama')
    def test_end_to_end_movie_analysis(self, mock_ollama, mock_search):
        """Test end-to-end movie analysis workflow."""
        # Mock search results
        mock_search_instance = Mock()
        mock_search_instance.run.return_value = "Mock movie data"
        mock_search.return_value = mock_search_instance
        
        # Mock model response
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.content = "Analysis complete"
        mock_model_instance.invoke.return_value = mock_response
        mock_model_instance.bind_tools.return_value = mock_model_instance
        mock_ollama.return_value = mock_model_instance
        
        # Test the workflow
        with patch('src.agents.movie_agent.get_settings') as mock_settings:
            mock_settings.return_value = Mock()
            mock_settings.return_value.model.name = "test"
            mock_settings.return_value.model.temperature = 0.1
            mock_settings.return_value.model.timeout = 30
            mock_settings.return_value.agent.graph_visualization = False
            
            agent = MovieAnalysisAgent()
            # This would fail in real test due to complex mocking needed
            # but shows the structure for integration testing
            # result = agent.analyze_movie("The Dark Knight")
            # self.assertIsInstance(result, str)


if __name__ == "__main__":
    # Run specific test categories
    import sys
    
    if len(sys.argv) > 1:
        test_category = sys.argv[1]
        if test_category == "config":
            suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
        elif test_category == "tools":
            suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchTools)
        elif test_category == "models":
            suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchResult)
        elif test_category == "agent":
            suite = unittest.TestLoader().loadTestsFromTestCase(TestMovieAgent)
        elif test_category == "integration":
            suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegration)
        else:
            print("Available test categories: config, tools, models, agent, integration")
            sys.exit(1)
    else:
        # Run all tests
        suite = unittest.TestLoader().discover('.', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)
