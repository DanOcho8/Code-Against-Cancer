from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cancer_type = models.CharField(max_length=100, blank=True, null=True)
    date_diagnosed = models.DateField(blank=True, null=True)
    cancer_stage = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    consent_to_text = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Donor(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"
