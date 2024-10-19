import json
import os
import random
import time
from unittest.mock import MagicMock, patch

import requests
from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.test import Client, TestCase
from django.urls import reverse

from CodeAgainstCancer.views import (
    about,
    contact,
    donate,
    homepageView,
    login_view,
    resources,
    searchRecipes,
    user_logout,
)


class ViewsTestCase(TestCase):
    """
    ViewsTestCase is a test case class that contains unit tests for the views in the application.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the test client and creates a test user along with
        a corresponding user profile. The user profile includes details such as
        cancer type, date diagnosed, cancer stage, and gender.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            cancer_type="Breast",
            date_diagnosed="2020-01-01",
            cancer_stage="Stage II",
            gender="Female",
        )

    def test_user_logout(self):
        """
        Test the user logout functionality.

        This test logs in a user with the username "testuser" and password "12345",
        then sends a GET request to the logout URL. It asserts that the response
        redirects to the home page.
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))

    def test_homepageView(self):
        """
        Tests the homepage view.

        This test ensures that the homepage view is accessible via a GET request,
        returns a status code of 200, and uses the correct template 'home.html'.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_login_view(self):
        """
        Test the login view.

        This test posts a username and password to the login view and asserts that
        the response redirects to the home page.

        Assertions:
            - The response should redirect to the home page.
        """
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "12345"}
        )
        self.assertRedirects(response, reverse("home"))

    @patch("CodeAgainstCancer.views.APIHandlerFactory.get_API_handler")
    def test_resources(self, mock_get_API_handler):
        """
        Test case for the resources view.

        This test case patches the `get_API_handler` method of the `APIHandlerFactory`
        to return mock handlers for PubMed and YouTube APIs. It then logs in a test
        user, makes a GET request to the `resources` view, and verifies the response.

        Methods:
            test_resources(mock_get_API_handler):
                Patches the API handler factory to return mock handlers, logs in a
                test user, makes a GET request to the `resources` view, and asserts
                the response status code and template used.
        """
        self.client.login(username="testuser", password="12345")

        # Mocking PubMed and YouTube API handlers
        mock_youtube_handler = MagicMock()
        mock_youtube_handler.fetch.return_value = {
            "items": [],
            "nextPageToken": None,
            "prevPageToken": None,
        }
        mock_pubmed_handler = MagicMock()
        mock_pubmed_handler.fetch.return_value = []

        # Mock API handler factory to return our mock handlers
        mock_get_API_handler.side_effect = [mock_youtube_handler, mock_pubmed_handler]

        # Make the request and check response
        response = self.client.get(reverse("resources"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/resources.html")

    def test_about(self):
        """
        Tests the 'about' view.

        This test performs a GET request to the 'about' URL and verifies that
        the response status code is 200 (OK) and the correct template
        'about/about.html' is used in the response.
        """
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about/about.html")

    def test_donate(self):
        """
        Test the donate view.

        This test ensures that the donate view is accessible via a GET request,
        returns a status code of 200, and uses the correct template 'donate/donate.html'.
        """
        response = self.client.get(reverse("donate"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "donate/donate.html")
