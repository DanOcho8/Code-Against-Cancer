from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Thread, Post
from accounts.models import UserProfile

class ForumTestCase(TestCase):
    def setUp(self):
        # Create a user and a profile for that user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            cancer_type='lung',
            date_diagnosed='2020-01-01',
            cancer_stage='Stage 2',
            gender='Male'
        )

        # Create a thread and a post
        self.thread = Thread.objects.create(title="Test Thread", created_at="2024-11-07")
        self.post = Post.objects.create(thread=self.thread, content="Test Post", author=self.user)

    def test_thread_list_page(self):
        # Test if thread list page renders correctly
        response = self.client.get(reverse('thread_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Threads")
        self.assertContains(response, self.thread.title)

    def test_create_thread_view(self):
        # Test thread creation
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('create_thread'), {'title': 'New Thread', 'content': 'Thread content'})
        self.assertEqual(response.status_code, 302)  # Redirect after thread creation
        self.assertTrue(Thread.objects.filter(title="New Thread").exists())

    def test_thread_detail_view(self):
        # Test thread detail view
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.thread.title)
        self.assertContains(response, self.post.content)

    def test_create_post_view(self):
        # Test creating a new post in a thread
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('create_post', args=[self.thread.pk]), {'content': 'New post content'})
        self.assertEqual(response.status_code, 302)  # Redirect after post creation
        self.assertTrue(Post.objects.filter(content='New post content').exists())

    def test_reply_to_post_view(self):
        # Test replying to a post
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('reply_to_post', args=[self.post.pk]), {'content': 'Reply content'})
        self.assertEqual(response.status_code, 302)  # Redirect after reply creation
        self.assertTrue(Post.objects.filter(content='Reply content', parent_post=self.post).exists())
