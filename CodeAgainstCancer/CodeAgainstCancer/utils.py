import logging


class LoggerSingleton:
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
            file_handler = logging.FileHandler('django_debug.log')
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter and set it for the handlers
            formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # Add the handlers to the logger instance
            cls._instance.addHandler(console_handler)
            cls._instance.addHandler(file_handler)

        # Return the single instance of the logger
        return cls._instance
