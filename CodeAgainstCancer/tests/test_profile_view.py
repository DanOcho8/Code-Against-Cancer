from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile
import json
import time
from django.conf import settings
import os

class ProfileViewTests(TestCase):
    
    def setUp(self):
        # Create a user and a profile for that user
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.profile = UserProfile.objects.create(
            user=self.user,
            cancer_type='lung',
            date_diagnosed='2020-01-01',
            cancer_stage='Stage 2',
            gender='Male'
        )

    def test_profile_view_loads_correct_cancer_information(self):
        """Test if the profile page loads correct information from cancer_information.json"""
        # Log the user in
        self.client.login(username='testuser', password='password123!')

        # Load the cancer information from the actual JSON file to compare
        json_path = os.path.join(settings.BASE_DIR, 'static/cancer_information.json')
        with open(json_path, 'r') as json_file:
            cancer_data = json.load(json_file)

        # Fetch the data specific to 'lung' cancer type from the JSON file
        expected_cancer_info = cancer_data['lung']

        # Send a GET request to the profile page
        response = self.client.get(reverse('profile'))

        # Ensure the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct dietary restrictions are displayed
        self.assertContains(response, expected_cancer_info['dietary_restrictions'])
        # Check if the recommended foods are displayed
        self.assertContains(response, expected_cancer_info['recommended_foods'])
        # Check if the special instructions are displayed
        self.assertContains(response, expected_cancer_info['special_instructions'])

class PerformanceTests(TestCase):

    def setUp(self):
        # Create a user and a profile for that user
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.profile = UserProfile.objects.create(
            user=self.user,
            cancer_type='lung',
            date_diagnosed='2020-01-01',
            cancer_stage='Stage 2',
            gender='Male'
        )
        # Log in the user
        self.client.login(username='testuser', password='password123!')
            
    def test_profile_page_load_time(self):
        """
        Test that the profile page loads within 3 seconds under normal load.
        """
        start_time = time.time()
        response = self.client.get(reverse('profile'))  
        load_time = time.time() - start_time
        self.assertEqual(response.status_code, 200)
        self.assertLess(load_time, 3)  # The page should load within 3 seconds

class ProfileSecurityTests(TestCase):

    def setUp(self):
        # Create a user and a profile for that user
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.profile = UserProfile.objects.create(
            user=self.user,
            cancer_type='lung',
            date_diagnosed='2020-01-01',
            cancer_stage='Stage 2',
            gender='Male'
        )
        self.client.login(username='testuser', password='password123!')

    @override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if 'django.middleware.csrf.CsrfViewMiddleware' not in mw])
    def test_profile_update_no_csrf_middleware(self):
        """
        Test that the profile update page is NOT protected against CSRF attacks when CSRF middleware is disabled.
        This simulates an environment without CSRF protection and expects the request to succeed.
        """
        response = self.client.post(reverse('update_profile'), {
            'cancer_type': 'breast',
            'cancer_stage': 'Stage 3',
        }, follow=True)

        # Assert that the request succeeds when CSRF is disabled
        self.assertEqual(response.status_code, 200)

    def test_profile_update_without_csrf_token(self):
        """
        Test that the profile update page rejects requests without a CSRF token.
        """
        # Log the user in and send a request without a CSRF token (using HTTP headers)
        self.client.cookies.pop('csrftoken')  # Remove the CSRF token

        response = self.client.post(reverse('update_profile'), {
            'cancer_type': 'breast',
            'cancer_stage': 'Stage 3',
        }, follow=True)

        # Assert that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, 403)
