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
    email = models.EmailField(max_length=254, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True, default="Anonymous")
    message = models.TextField(blank=True, null=True, max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)
    
    def __str__(self):
        verification_status = "Verified" if self.validated else "Not Verified"
        amount_display = f"${self.amount}" if self.amount else "No Amount"
        return f"{self.name} ({self.email}) - {amount_display} - {verification_status}"