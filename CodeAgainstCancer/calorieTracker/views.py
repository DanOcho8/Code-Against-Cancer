from django.shortcuts import render, redirect
from .models import CalorieIntakeEntry, FoodItem
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import AddCalorieEntryForm

@login_required(login_url="login")
def calorie_tracker(request):

    # Fetch user's profile from accounts app
    user = request.user
    selected_date = request.GET.get('date', timezone.now().date())
    calorie_entries = CalorieIntakeEntry.objects.filter(user=user, date=selected_date)


    # Calculate total calories for the day
    total_calories = sum(entry.calculated_calories for entry in calorie_entries)
    
    form = AddCalorieEntryForm()
    
    context = {
        'calorie_entries': calorie_entries,
        'total_calories': total_calories,
        'selected_date': selected_date,
        'form': form,
    }
    
    return render(request, 'calorie/calorie.html', context)


@login_required(login_url="login")
def add_calorie_entry(request):
    if request.method == "POST":
        form = AddCalorieEntryForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            amount_in_grams = form.cleaned_data['amount_in_grams']
            calories_per_gram = form.cleaned_data['calories_per_gram']
            date = form.cleaned_data['date']

            # Get or create the food item in the database
            food_item, created = FoodItem.objects.get_or_create(name=food_name, defaults={'calories_per_gram': calories_per_gram})

            # Calculate calories
            calculated_calories = food_item.calories_per_gram * amount_in_grams


            CalorieIntakeEntry.objects.create(
                user=request.user,
                food_item=food_item,
                amount_in_grams=amount_in_grams,
                calculated_calories=calculated_calories,
                date=date
            )

            return redirect(f"{request.path.replace('/add/', '/calorie/')}?date={date}")
    return redirect('calorieTracker:calorie_tracker')

@login_required(login_url="login")
def delete_calorie_entry(request, entry_id):

    selected_date = request.GET.get('date', timezone.now().date())
    entry = get_object_or_404(CalorieIntakeEntry, id=entry_id, user=request.user)
    entry.delete()


    return redirect(f"{request.build_absolute_uri('/calorieTracker/calorie/')}?date={selected_date}")

class EditCalorieEntryForm(forms.ModelForm):
    class Meta:
        model = CalorieIntakeEntry
        fields = ['food_item', 'amount_in_grams', 'date']
        
    food_item = forms.CharField(max_length=100)

@login_required(login_url="login")
def edit_calorie_entry(request, entry_id):
    entry = get_object_or_404(CalorieIntakeEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = EditCalorieEntryForm(request.POST, instance=entry)
        if form.is_valid():
            # Update the entry with the new data
            entry = form.save(commit=False)
            
            # Update the calculated calories if necessary
            food_item = form.cleaned_data['food_item']
            entry.food_item, created = FoodItem.objects.get_or_create(name=food_item)
            entry.calculated_calories = entry.food_item.calories_per_gram * entry.amount_in_grams
            entry.save()

            # Redirect to the calorie tracker page after saving
            return redirect('calorie_tracker')
    else:
        # Prepopulate the form with the current entry data
        form = EditCalorieEntryForm(instance=entry)
        form.initial['food_item'] = entry.food_item.name  # Set the initial food item name

    return render(request, 'calorie/edit_entry.html', {'form': form, 'entry': entry})