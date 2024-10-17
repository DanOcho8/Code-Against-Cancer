from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile


class ResourcesViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.profile = UserProfile.objects.create(
            user=self.user, 
            cancer_type='Lung', 
            cancer_stage='Stage 2', 
            date_diagnosed='2020-01-01', 
            gender='Male'
        )

    def test_redirect_if_not_logged_in(self):
        """Test that user is redirected to login if not authenticated"""
        response = self.client.get(reverse('resources'))
        # Ensure that unauthenticated users are redirected to the login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('resources')}")

    def test_authenticated_user_access_resources(self):
        """Test resource page access with authenticated user"""
        self.client.login(username='testuser', password='password123!')
        response = self.client.get(reverse('resources'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/resources.html')