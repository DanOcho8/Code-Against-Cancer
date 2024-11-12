from django.shortcuts import render, redirect
from .models import CalorieIntakeEntry, FoodItem
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def calorie_tracker(request):

    # Fetch user's profile from accounts app
    user = request.user
    selected_date = request.GET.get('date', timezone.now().date())
    calorie_entries = CalorieIntakeEntry.objects.filter(user=user, date=selected_date)


    # Calculate total calories for the day
    total_calories = sum(entry.calculated_calories for entry in calorie_entries)
    
    context = {
        'calorie_entries': calorie_entries,
        'total_calories': total_calories,
        'selected_date': selected_date,
    }
    
    return render(request, 'calorietracker.html', context)
