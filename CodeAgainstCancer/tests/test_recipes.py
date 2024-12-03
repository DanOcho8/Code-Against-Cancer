import time
import requests
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile
from unittest.mock import patch
from django.contrib import messages


class SearchRecipesViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.profile = UserProfile.objects.create(
            user=self.user, 
            cancer_type='Lung', 
            cancer_stage='Stage 2', 
            date_diagnosed='2020-01-01', 
            gender='Male'
        )
        self.url = reverse('searchRecipes')

    @patch('requests.get')
    def test_random_recipes(self, mock_get):
        """Test fetching random recipes when no query is provided"""
        # Simulate login
        self.client.login(username='testuser', password='password123!')

        mock_get.return_value.json.return_value = {
            'hits': [{'recipe': {'label': 'Recipe1'}}, {'recipe': {'label': 'Recipe2'}}],
            'count': 1000
        }
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe.html')
        self.assertContains(response, 'Recipe1')
        self.assertContains(response, 'Recipe2')

    @patch('requests.get')
    def test_search_recipes_with_query(self, mock_get):
        """Test fetching recipes based on query"""
        # Simulate login
        self.client.login(username='testuser', password='password123!')

        mock_get.return_value.json.return_value = {
            'hits': [{'recipe': {'label': 'Chicken Soup'}}, {'recipe': {'label': 'Pasta'}}],
            'count': 2
        }
        response = self.client.get(self.url, {'query': 'chicken'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Soup')
        self.assertContains(response, 'Pasta')
        
        
    @patch('requests.get')
    def test_RecipeLoadTime(self, mock_get):
        """Test the load time of the recipe page"""
        # Simulate login
        self.client.login(username='testuser', password='password123!')

        # Mock the response for the recipes API
        mock_get.return_value.json.return_value = {
            'hits': [{'recipe': {'label': 'Recipe1'}}, {'recipe': {'label': 'Recipe2'}}],
            'count': 1000
        }

        query = "chicken"

        start_time = time.time()
        # Send a GET request to the recipe page
        response = self.client.get(self.url, {'query': query})
        load_time = time.time() - start_time
        self.assertEqual(response.status_code, 200)
        self.assertLess(load_time, 2, f"Page load time exceeded 2 seconds: {load_time:.2f} seconds")


        print(f"Load time for the recipe page: {load_time:.2f} seconds")
        
        
    def test_redirect_if_not_logged_in(self):
        """Test that user is redirected to login if not authenticated"""
        response = self.client.get(self.url)  # Attempt to access the recipes page
        # Ensure that unauthenticated users are redirected to the login page
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        
        
    @patch('requests.get')
    def test_no_recipes_found(self, mock_get):
        """Test the case when no recipes are found"""
        # Simulate login
        self.client.login(username='testuser', password='password123!')

        # Mock the response for the recipes API with empty results
        mock_get.return_value.json.return_value = {
            'hits': [],
            'count': 0
        }
    
        response = self.client.get(self.url, {'query': 'some query'})  # Use a sample query
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes found")  # Check for the message
        self.assertEqual(response.context['recipes'], [])
        
    @patch('requests.get')
    def test_api_failure_handling(self, mock_get):
        """Test handling of API failures when fetching recipes."""
        # Simulate login
        self.client.login(username='testuser', password='password123!')

        # Simulate API failure
        mock_get.side_effect = requests.exceptions.RequestException("API failure")

        # Make a GET request to the searchRecipes view
        response = self.client.get(self.url, {'query': 'chicken'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the error message is in the response
        self.assertContains(response, "Unable to fetch recipes at this time, API failed")

        # Verify that the recipes context is an empty list
        self.assertEqual(response.context['recipes'], [])

        # Check that pagination indicators are set correctly in the context
        self.assertFalse(response.context['hasNextPage'])  # Ensure next page is not available
        self.assertFalse(response.context['hasPrevPage'])   # Ensure previous page is not available
        
        # Check that the message was added to the messages framework
        self.assertEqual(len(list(messages.get_messages(response.wsgi_request))), 1)
        message = list(messages.get_messages(response.wsgi_request))[0]
        self.assertEqual(message.message, "Unable to fetch recipes at this time, API failed")
