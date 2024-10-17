from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile  # Assuming UserProfile exists
from django.core.files.uploadedfile import SimpleUploadedFile

class TestSignupView(TestCase):  # Ensure class starts with 'Test'

    def setUp(self):
        # You can add setup steps if needed
        pass

    def test_signup_view_renders_correct_template(self):
        """Test if the signup view renders the correct template for a GET request"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form_post_valid_data(self):
        """Test successful signup with valid data"""
        form_data = {
            'username': 'newuser',
            'password1': 'securepassword123!',
            'password2': 'securepassword123!',
        }
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_signup_form_post_invalid_data(self):
        """Test signup failure with invalid data"""
        form_data = {
            'username': 'newuser',
            'password1': 'securepassword123!',
            'password2': 'differentpassword',  # Passwords do not match
        }
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")

    def test_signup_with_uploaded_file(self):
        """Test signup with a valid file upload"""
        form_data = {
            'username': 'fileuploaduser',
            'password1': 'securepassword123!',
            'password2': 'securepassword123!',
        }
        uploaded_file = SimpleUploadedFile('test_file.txt', b'This is the file content.')
        form_data['profile_pic'] = uploaded_file  # Assuming the form has a profile picture field
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='fileuploaduser')
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_signup_flash_message_on_success(self):
        """Test that a success message is displayed on successful signup"""
        form_data = {
            'username': 'messageuser',
            'password1': 'securepassword123!',
            'password2': 'securepassword123!',
        }
        response = self.client.post(reverse('signup'), form_data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Registration successful!')
