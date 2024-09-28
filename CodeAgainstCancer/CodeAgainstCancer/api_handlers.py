from abc import ABC, abstractmethod

import requests
from django.conf import settings

from .utils import LoggerSingleton


# Base class for all API handlers (Template Method Pattern)
class APIHandler(ABC):
    """
    APIHandler is an abstract base class that provides a template for handling API requests.

    Methods
    -------
    __init__():
        Initializes the APIHandler with a LoggerSingleton instance for logging.

    fetch(query, **kwargs):
        Constructs the API request URL and parameters, makes the request, and handles the response.
        Logs the request and response status.
        Parameters:
            query (str): The query string for the API request.
            **kwargs: Additional parameters for the API request.
        Returns:
            dict: Parsed JSON response from the API, or an empty dictionary if an error occurs.

    get_url():
        Abstract method to be implemented by subclasses to provide the API endpoint URL.
        Returns:
            str: The API endpoint URL.

    get_params(query, **kwargs):
        Abstract method to be implemented by subclasses to construct the parameters for the API request.
        Parameters:
            query (str): The query string for the API request.
            **kwargs: Additional parameters for the API request.
        Returns:
            dict: The parameters for the API request.

    parse_response(data):
        Abstract method to be implemented by subclasses to parse the API response data.
        Parameters:
            data (dict): The JSON response data from the API.
        Returns:
            dict: The parsed response data.
    """

    def __init__(self):
        self.logging = LoggerSingleton()

    def fetch(self, query, **kwargs):
        url = self.get_url()
        params = self.get_params(query, **kwargs)
        self.logging.debug(f"Making API request to {url} with params {params}")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            self.logging.info(f"API request to {url} was successful.")
            return self.parse_response(response.json())
        except requests.RequestException as e:
            self.logging.error(f"Error fetching data from {url}: {e}")
            return {}

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def get_params(self, query, **kwargs):
        pass

    @abstractmethod
    def parse_response(self, data):
        pass


# Handler for YouTube API
class YouTubeAPIHandler(APIHandler):
    """
    A handler for interacting with the YouTube Data API v3.

    Methods
    -------
    get_url():
        Returns the URL endpoint for the YouTube search API.

    get_params(query, **kwargs):
        Constructs and returns the parameters for the API request.

        Parameters:
        - query (str): The search query string.
        - **kwargs: Additional optional parameters.
            - page_token (str, optional): Token for the next page of results.

        Returns:
        - dict: A dictionary of parameters to be sent with the API request.

    parse_response(data):
        Parses the API response data and extracts relevant information.

        Parameters:
        - data (dict): The JSON response from the YouTube API.

        Returns:
        - dict: A dictionary containing:
            - items (list): List of videos.
            - nextPageToken (str, optional): Token for the next page of results.
            - prevPageToken (str, optional): Token for the previous page of results.
    """

    def get_url(self):
        return "https://www.googleapis.com/youtube/v3/search"

    def get_params(self, query, **kwargs):
        params = {
            "part": "snippet",
            "q": query,
            "maxResults": 3,
            "order": "relevance",
            "key": settings.YOUTUBE_API_KEY,
            "videoEmbeddable": "true",
            "type": "video",
        }
        if "page_token" in kwargs:
            params["pageToken"] = kwargs["page_token"]
        return params

    def parse_response(self, data):
        return {
            "items": data.get("items", []),  # List of videos
            "nextPageToken": data.get("nextPageToken"),  # Token for the next page
            "prevPageToken": data.get(
                "prevPageToken"
            ),  # Token for the previous page (if applicable)
        }


# Handler for PubMed API
class PubMedAPIHandler(APIHandler):
    """
    Handler for interacting with the PubMed API.

    Methods
    -------
    get_url():
        Returns the URL for the PubMed API endpoint.

    get_params(query, **kwargs):
        Constructs and returns the parameters for the API request.

        Parameters:
        query (str): The search term to query PubMed.
        **kwargs: Additional optional parameters.
            - max_results (int): Maximum number of results to return (default is 5).

        Returns:
        dict: A dictionary of parameters for the API request.

    parse_response(data):
        Parses the response from the PubMed API.

        Parameters:
        data (dict): The JSON response data from the PubMed API.

        Returns:
        dict: A dictionary containing the parsed article details if article IDs are found,
              otherwise an empty dictionary.
    """

    def get_url(self):
        return "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    def get_params(self, query, **kwargs):
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": kwargs.get("max_results", 5),
            "retmode": "json",
            "sort": "relevance",
        }
        return params

    def parse_response(self, data):
        article_ids = data.get("esearchresult", {}).get("idlist", [])

        # If there are article IDs, use the PubMedSummaryHandler to fetch the details
        if article_ids:
            summary_handler = PubMedSummaryHandler()
            return summary_handler.fetch(article_ids)
        return {}


# Handler for PubMed API to get summaries
class PubMedSummaryHandler(APIHandler):
    """
    PubMedSummaryHandler is a class that handles interactions with the PubMed eSummary API.

    Methods:
        get_url():
            Returns the URL for the PubMed eSummary API.

        get_params(article_ids, **kwargs):
            Builds and returns the parameters required to fetch details for a list of article IDs.
            Args:
                article_ids (list): A list of PubMed article IDs.
                **kwargs: Additional keyword arguments.
            Returns:
                dict: A dictionary containing the parameters for the API request.

        parse_response(data):
            Parses the response data from the PubMed eSummary API.
            Args:
                data (dict): The response data from the API.
            Returns:
                dict: A dictionary containing the detailed article information.
    """

    def get_url(self):
        return "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    def get_params(self, article_ids, **kwargs):
        # Build parameters to fetch details for the list of article IDs
        params = {
            "db": "pubmed",
            "id": ",".join(article_ids),  # Join IDs with commas
            "retmode": "json",
        }
        return params

    def parse_response(self, data):
        # Return the detailed article information from esummary
        return data.get("result", {})


# TODO: test this class
# TODO: write documentation for this class
# Handler for Edamam Recipe API
class EdamamAPIHandler(APIHandler):
    def get_url(self):
        return f"https://api.edamam.com/search"

    def get_params(self, query, **kwargs):
        params = {
            "q": query,
            "app_id": settings.APP_ID,
            "app_key": settings.API_KEY,
            "from": kwargs.get("from_recipes", 0),
            "to": kwargs.get("to_recipes", 6),
        }
        return params

    def parse_response(self, data):
        return data.get("hits", [])


# Factory pattern to return the correct API handler
class ResourceFactory:
    """
    ResourceFactory is a factory class that provides a method to get the appropriate resource handler
    based on the resource type.

    Methods:
        get_resource_handler(resource_type: str):
            Static method that returns an instance of the appropriate handler class based on the
            provided resource type. The supported resource types are "video", "article", and "recipe".
            Raises a ValueError if an unknown resource type is provided.

            Parameters:
                resource_type (str): The type of resource for which a handler is needed.

            Returns:
                An instance of the appropriate handler class (YouTubeAPIHandler, PubMedAPIHandler,
                or EdamamAPIHandler).

            Raises:
                ValueError: If the provided resource type is not supported.
    """

    @staticmethod
    def get_resource_handler(resource_type):
        if resource_type == "video":
            return YouTubeAPIHandler()
        elif resource_type == "article":
            return PubMedAPIHandler()
        elif resource_type == "recipe":
            return EdamamAPIHandler()
        else:
            raise ValueError("Unknown resource type")
