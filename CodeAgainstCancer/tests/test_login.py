from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile

class LoginViewTests(TestCase):

    def setUp(self):
        # Create a user and a profile for that user
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.profile = UserProfile.objects.create(
            user=self.user,
            cancer_type='Lung',
            date_diagnosed='2020-01-01',
            cancer_stage='Stage 1',
            gender='Male'
        )

    def test_valid_login(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        print(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have entered an invalid username or password')

    def test_redirect_incomplete_profile(self):
        """Test redirect to profile completion if user profile is incomplete"""
        self.profile.cancer_type = ''  # Mark cancer_type as empty, indicating an incomplete profile
        self.profile.save()

        # Logging in attempt
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123!'
        })
        self.assertRedirects(response, reverse('update_profile'))  
        # If cancer_type is empty, they should be redirected to updating profile view
