from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cancer_type = models.CharField(max_length=100, blank=True, null=True)
    date_diagnosed = models.DateField(blank=True, null=True)
    cancer_stage = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    