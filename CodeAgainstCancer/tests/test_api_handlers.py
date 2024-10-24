import unittest
from unittest.mock import MagicMock, patch

import requests
from django.conf import settings

from CodeAgainstCancer.api_handlers import (
    APIHandlerFactory,
    EdamamAPIHandler,
    PubMedAPIHandler,
    PubMedSummaryHandler,
    YouTubeAPIHandler,
)


class BaseAPIHandlerTest(unittest.TestCase):
    """Base class for common functionality shared among tests"""

    def mock_api_response(self, mock_get, json_data, status_code=200):
        """Helper method to mock API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = json_data
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response


class TestYouTubeAPIHandler(BaseAPIHandlerTest):
    @patch("requests.Session.get")
    def test_fetch_success_returns_expected_data(self, mock_get):
        self.mock_api_response(
            mock_get,
            {
                "items": [{"id": "video1"}, {"id": "video2"}],
                "nextPageToken": "next_token",
                "prevPageToken": "prev_token",
            },
        )

        handler = YouTubeAPIHandler()
        result = handler.fetch("cancer research")

        self.assertEqual(result["items"], [{"id": "video1"}, {"id": "video2"}])
        self.assertEqual(result["nextPageToken"], "next_token")
        self.assertEqual(result["prevPageToken"], "prev_token")

    @patch("requests.Session.get")
    def test_fetch_failure_returns_empty_dict(self, mock_get):
        mock_get.side_effect = requests.RequestException("API request failed")

        handler = YouTubeAPIHandler()
        result = handler.fetch("cancer research")

        self.assertEqual(result, {})


class TestPubMedAPIHandler(BaseAPIHandlerTest):
    @patch("requests.Session.get")
    def test_fetch_success_returns_details(self, mock_get):
        self.mock_api_response(
            mock_get, {"esearchresult": {"idlist": ["12345", "67890"]}}
        )

        handler = PubMedAPIHandler()
        with patch.object(
            PubMedSummaryHandler, "fetch", return_value={"result": "details"}
        ):
            result = handler.fetch("cancer research")

        self.assertEqual(result, {"result": "details"})

    @patch("requests.Session.get")
    def test_fetch_failure_returns_empty_dict(self, mock_get):
        mock_get.side_effect = requests.RequestException("API request failed")

        handler = PubMedAPIHandler()
        result = handler.fetch("cancer research")

        self.assertEqual(result, {})


class TestEdamamAPIHandler(BaseAPIHandlerTest):
    @patch("requests.Session.get")
    def test_fetch_success_returns_recipe_list(self, mock_get):
        self.mock_api_response(
            mock_get, {"hits": [{"recipe": "recipe1"}, {"recipe": "recipe2"}]}
        )

        handler = EdamamAPIHandler()
        result = handler.fetch("chicken")

        self.assertEqual(result, [{"recipe": "recipe1"}, {"recipe": "recipe2"}])

    @patch("requests.Session.get")
    def test_fetch_failure_returns_empty_dict(self, mock_get):
        mock_get.side_effect = requests.RequestException("API request failed")

        handler = EdamamAPIHandler()
        result = handler.fetch("chicken")

        self.assertEqual(result, {})


class TestAPIHandlerFactory(unittest.TestCase):
    def test_get_API_handler_video_returns_YouTubeAPIHandler(self):
        handler = APIHandlerFactory.get_API_handler("video")
        self.assertIsInstance(handler, YouTubeAPIHandler)

    def test_get_API_handler_article_returns_PubMedAPIHandler(self):
        handler = APIHandlerFactory.get_API_handler("article")
        self.assertIsInstance(handler, PubMedAPIHandler)

    def test_get_API_handler_recipe_returns_EdamamAPIHandler(self):
        handler = APIHandlerFactory.get_API_handler("recipe")
        self.assertIsInstance(handler, EdamamAPIHandler)

    def test_get_API_handler_invalid_raises_ValueError(self):
        with self.assertRaises(ValueError):
            APIHandlerFactory.get_API_handler("invalid")


if __name__ == "__main__":
    unittest.main()
