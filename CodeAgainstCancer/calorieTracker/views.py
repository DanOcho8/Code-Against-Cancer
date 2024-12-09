from django.shortcuts import render, redirect
from .models import CalorieIntakeEntry, FoodItem, SearchedFoodItem
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import AddCalorieEntryForm
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.urls import reverse
from django.http import Http404


@login_required(login_url="login")
def calorie_tracker(request):
    user = request.user
    selected_date = request.GET.get('date', timezone.now().date())

    # Ensure selected_date is always a date object
    if isinstance(selected_date, str):
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    calorie_entries = CalorieIntakeEntry.objects.filter(user=user, date=selected_date)
    searched_food_items = SearchedFoodItem.objects.filter(user=user, date=selected_date)

    total_calories = (
        sum(entry.calculated_calories for entry in calorie_entries) + 
        sum(item.total_calories for item in searched_food_items)
    )
    total_protein = (
        sum(entry.food_item.protein_per_gram * entry.amount_in_grams for entry in calorie_entries) + 
        sum(item.total_protein for item in searched_food_items)
    )

    context = {
        'calorie_entries': calorie_entries,
        'searched_food_items': searched_food_items,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'selected_date': selected_date,
        'today': timezone.now().date(),
        'yesterday': timezone.now().date() - timedelta(days=1),
        'tomorrow': timezone.now().date() + timedelta(days=1),
    }

    return render(request, 'calorie/calorie.html', context)



@login_required(login_url="login")
def add_calorie_entry(request):
    user = request.user
    selected_date = request.GET.get("date") or request.POST.get("date") or timezone.now().date()
    query = request.GET.get("query", "")
    results = []
    redirect_url = f"{reverse('calorieTracker:calorie_tracker')}?date={selected_date}"

    if request.method == "GET" and query:
        # Handle USDA API search
        api_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&api_key={settings.USDA_API_KEY}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                results = [
                    {
                        "description": food["description"],
                        "calories": next((n["value"] for n in food.get("foodNutrients", []) if n["nutrientName"] == "Energy"), 0),
                        "protein": next((n["value"] for n in food.get("foodNutrients", []) if n["nutrientName"] == "Protein"), 0),
                        "picture": food.get("foodCategoryImage"),  # Assuming USDA provides image URLs here
                    }
                    for food in data.get("foods", [])
                ]
            else:
                results = []
        except requests.exceptions.RequestException:
            results = []
            
            
    elif request.method == "POST":
        
        if request.POST.get("food_name") and request.POST.get("searched_calories_per_gram"):
            food_name = request.POST.get("food_name")
            searched_calories_per_gram = float(request.POST.get("searched_calories_per_gram", 0)) / 100
            searched_protein_per_gram = float(request.POST.get("searched_protein_per_gram", 0)) / 100
            amount_in_grams = float(request.POST.get("amount_in_grams", 0))

            # Calculate total calories and protein
            total_calories = searched_calories_per_gram * amount_in_grams
            total_protein = searched_protein_per_gram * amount_in_grams

            # Save the searched food item
            SearchedFoodItem.objects.create(
                user=user,
                description=food_name,
                total_calories=total_calories,
                total_protein=total_protein,
                date=selected_date,
            )

            return redirect(redirect_url)

        else:
            # Handle manual food item entry
            form = AddCalorieEntryForm(request.POST)
            if form.is_valid():
                food_name = form.cleaned_data["food_name"]
                amount_in_grams = form.cleaned_data["amount_in_grams"]
                calories_per_gram = form.cleaned_data["calories_per_gram"]
                protein_per_gram = form.cleaned_data["protein_per_gram"]

                # Add or retrieve the food item
                food_item, created = FoodItem.objects.get_or_create(
                    name=food_name,
                    defaults={
                                "calories_per_gram": calories_per_gram,
                                "protein_per_gram": protein_per_gram,
                        }
                )

                # Calculate total calories
                calculated_calories = food_item.calories_per_gram * amount_in_grams
                calculated_protein = food_item.protein_per_gram * amount_in_grams

                # Create the calorie entry
                CalorieIntakeEntry.objects.create(
                    user=request.user,
                    food_item=food_item,
                    amount_in_grams=amount_in_grams,
                    calculated_calories=calculated_calories,
                    calculated_protein=calculated_protein,
                    date=selected_date,
                )

            return redirect(redirect_url)

    context = {
        "selected_date": selected_date,
        "query": query,
        "results": results,
        "form": AddCalorieEntryForm(),
    }

    return render(request, "calorie/add_entry.html", context)


@login_required(login_url="login")
def delete_calorie_entry(request, entry_id):

    selected_date = request.GET.get('date')
    if selected_date:
        try:
            # Ensure selected_date is in "YYYY-MM-DD" format if passed
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            # In case of an incorrect format, default to today's date
            selected_date = timezone.now().date().strftime('%Y-%m-%d')
    else:
        selected_date = timezone.now().date().strftime('%Y-%m-%d')
    entry = CalorieIntakeEntry.objects.filter(id=entry_id, user=request.user).first()
    
    if entry:
        entry.delete()
    else:
        # If not found in CalorieIntakeEntry, try SearchedFoodItem
        searched_entry = SearchedFoodItem.objects.filter(id=entry_id, user=request.user).first()
        if searched_entry:
            searched_entry.delete()
        else:
            # If the entry doesn't exist in either table, raise a 404
            raise Http404("Entry not found.")


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