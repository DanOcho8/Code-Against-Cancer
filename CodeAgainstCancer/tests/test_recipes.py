from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile
from unittest.mock import patch

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
