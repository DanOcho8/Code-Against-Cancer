import logging
from functools import wraps

from django.core.cache import cache


class LoggerSingleton:
    """
    LoggerSingleton is a singleton class that provides a single instance of a logger.

    Attributes:
        _instance (logging.Logger): The single instance of the logger.

    Methods:
        __new__(cls):
            Creates and returns the single instance of the logger. If the instance
            does not exist, it sets up the logger with a console handler and a file
            handler, both with DEBUG level logging. The log messages are formatted
            to include the timestamp, filename, line number, log level, and message.
    """

    _instance = None  # This class attribute holds the single instance

    def __new__(cls):
        if cls._instance is None:  # Check if the instance already exists
            # If no instance exists, create one
            cls._instance = logging.getLogger(__name__)

            # Set up the logger level and handlers
            cls._instance.setLevel(logging.DEBUG)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # Create file handler (logs to file)
            file_handler = logging.FileHandler("django_debug.log")
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter and set it for the handlers
            formatter = logging.Formatter(
                "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # Add the handlers to the logger instance
            cls._instance.addHandler(console_handler)
            cls._instance.addHandler(file_handler)

        # Return the single instance of the logger
        return cls._instance


def cache_results(timeout=300):
    """
    A decorator to cache the results of a function for a specified timeout period.

    Args:
        timeout (int, optional): The cache timeout period in seconds. Defaults to 300 seconds.

    Returns:
        function: The decorated function with caching enabled.

    The decorator generates a cache key based on the function name, arguments, and keyword arguments.
    If a cached result exists for the generated key, it returns the cached result.
    Otherwise, it calls the function, caches the result, and then returns the result.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a cache key based on the function name, args, and kwargs
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached_result = cache.get(cache_key)
            # If a cached result exists, return it
            if cached_result:
                return cached_result
            result = func(*args, **kwargs)
            # Cache the result with the specified timeout
            cache.set(cache_key, result, timeout)
            return result

        return wrapper

    return decorator
