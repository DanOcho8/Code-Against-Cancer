from django.shortcuts import render, redirect
from .models import CalorieIntakeEntry, FoodItem
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django import forms

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
    
    return render(request, 'calorie/calorie.html', context)


@login_required(login_url="login")
def add_calorie_entry(request):
    if request.method == "POST":
        form = AddCalorieEntryForm(request.POST)
        if form.is_valid():
            # Get data from the form
            food_name = form.cleaned_data['food_name']
            amount_in_grams = form.cleaned_data['amount_in_grams']
            date = form.cleaned_data['date']

            # Get or create the food item in the database
            food_item, created = FoodItem.objects.get_or_create(name=food_name)

            # Calculate calories (you may need to adjust this depending on your calorie calculation)
            calculated_calories = food_item.calories_per_gram * amount_in_grams

            # Create a new CalorieIntakeEntry for the logged-in user
            CalorieIntakeEntry.objects.create(
                user=request.user,
                food_item=food_item,
                amount_in_grams=amount_in_grams,
                calculated_calories=calculated_calories,
                date=date
            )

            # Redirect to the calorie tracker page after saving
            return redirect('calorie_tracker')
    else:
        form = AddCalorieEntryForm()

    return render(request, 'calorie/add_entry.html', {'form': form})

class AddCalorieEntryForm(forms.Form):
    food_name = forms.CharField(max_length=100)
    amount_in_grams = forms.DecimalField(max_digits=5, decimal_places=2)
    date = forms.DateField(widget=forms.SelectDateWidget)

