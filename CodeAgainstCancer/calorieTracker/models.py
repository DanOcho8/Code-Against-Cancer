from django.db import models
from django.contrib.auth.models import User  # Or import your custom User model if you have one

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories_per_gram = models.DecimalField(max_digits=5, decimal_places=2)
    is_custom = models.BooleanField(default=False)  # True if manually added by the user

class CalorieIntakeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    amount_in_grams = models.DecimalField(max_digits=5, decimal_places=2)
    calculated_calories = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
