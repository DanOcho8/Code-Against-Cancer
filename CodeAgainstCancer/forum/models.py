from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Thread(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('thread_detail', kwargs={'pk': self.pk})

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey('self', null=True, blank=True, related_name='post_replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Reply(models.Model):
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
