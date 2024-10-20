import logging
import unittest
from unittest.mock import MagicMock, patch

from CodeAgainstCancer.utils import LoggerSingleton, cache_results


class TestLoggerSingleton(unittest.TestCase):
    """
    Unit tests for the LoggerSingleton class.

    TestLoggerSingleton:
        Tests for the LoggerSingleton class to ensure it behaves as a singleton and is properly configured.

        Methods:
            test_singleton_instance(mock_get_logger):
                Tests that the LoggerSingleton class returns the same instance every time it is instantiated.
                Mocks the getLogger method from the logging module to verify that the logger instance is the same.

            test_logger_setup(mock_get_logger, mock_stream_handler, mock_file_handler):
                Tests that the LoggerSingleton class sets up the logger correctly.
                Mocks the getLogger, StreamHandler, and FileHandler methods from the logging module to verify that the logger is configured with the correct level, handlers, and formatters.
    """

    @patch("CodeAgainstCancer.utils.logging.getLogger")
    def test_singleton_instance(self, mock_get_logger):
        # Reset the singleton instance
        LoggerSingleton._instance = None

        # Mock the logger instance
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Get the logger instance
        logger1 = LoggerSingleton()
        logger2 = LoggerSingleton()

        # Check that the logger instance is the same
        self.assertIs(logger1, logger2)
        mock_get_logger.assert_called_once_with("CodeAgainstCancer.utils")

    @patch("CodeAgainstCancer.utils.logging.FileHandler")
    @patch("CodeAgainstCancer.utils.logging.StreamHandler")
    @patch("CodeAgainstCancer.utils.logging.getLogger")
    def test_logger_setup(
        self, mock_get_logger, mock_stream_handler, mock_file_handler
    ):
        # Reset the singleton instance
        LoggerSingleton._instance = None

        # Mock the logger and handlers
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_stream_handler_instance = MagicMock()
        mock_file_handler_instance = MagicMock()
        mock_stream_handler.return_value = mock_stream_handler_instance
        mock_file_handler.return_value = mock_file_handler_instance

        # Get the logger instance
        LoggerSingleton()

        # Check that the logger level is set to DEBUG
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)

        # Check that the handlers are added to the logger
        mock_logger.addHandler.assert_any_call(mock_stream_handler_instance)
        mock_logger.addHandler.assert_any_call(mock_file_handler_instance)

        # Check that the handlers are set to DEBUG level
        mock_stream_handler_instance.setLevel.assert_called_once_with(logging.DEBUG)
        mock_file_handler_instance.setLevel.assert_called_once_with(logging.DEBUG)

        # Check that the formatter is set for the handlers
        self.assertTrue(mock_stream_handler_instance.setFormatter.called)
        self.assertTrue(mock_file_handler_instance.setFormatter.called)


class TestCacheResults(unittest.TestCase):
    """
    Unit tests for the cache_results decorator in the CodeAgainstCancer.utils module.

    Classes:
        TestCacheResults: Contains unit tests for the cache_results decorator.

    Methods:
        test_cache_results_decorator(self, mock_cache):
            Tests the cache_results decorator to ensure it caches the result of the decorated function
            with the specified timeout and generates the correct cache key.

        test_cache_results_decorator_with_cached_value(self, mock_cache):
            Tests the cache_results decorator to ensure it returns the cached result if available
            and does not call the cache set method.
    """

    @patch("CodeAgainstCancer.utils.cache")
    def test_cache_results_decorator(self, mock_cache):
        # Mock the cache get and set methods
        mock_cache.get.return_value = None

        @cache_results(timeout=100)
        def sample_function(x, y):
            return x + y

        # Call the decorated function
        result = sample_function(1, 2)

        # Check that the result is correct
        self.assertEqual(result, 3)

        # Check that the cache key is generated correctly
        expected_cache_key = "sample_function:(1, 2):{}"
        mock_cache.get.assert_called_once_with(expected_cache_key)

        # Check that the result is cached with the specified timeout
        mock_cache.set.assert_called_once_with(expected_cache_key, 3, 100)

    @patch("CodeAgainstCancer.utils.cache")
    def test_cache_results_decorator_with_cached_value(self, mock_cache):
        # Mock the cache get method to return a cached value
        mock_cache.get.return_value = 5

        @cache_results(timeout=100)
        def sample_function(x, y):
            return x + y

        # Call the decorated function
        result = sample_function(1, 2)

        # Check that the cached result is returned
        self.assertEqual(result, 5)

        # Check that the cache set method is not called
        mock_cache.set.assert_not_called()


if __name__ == "__main__":
    unittest.main()
