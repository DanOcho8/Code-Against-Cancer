from django.shortcuts import render, redirect
from .models import CalorieIntakeEntry, FoodItem, SearchedFoodItem, CalorieCalculatorEntry
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import AddCalorieEntryForm, CalorieCalculator
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.urls import reverse
from django.http import Http404, HttpResponseNotAllowed
from decimal import Decimal
from django.shortcuts import get_object_or_404


@login_required(login_url="login")
def calorie_tracker(request):
    user = request.user
    selected_date = request.GET.get("date")
    
    # Try to retrieve existing calculator entry for the user
    try:
        calculator_entry = CalorieCalculatorEntry.objects.get(user=user)
        form = CalorieCalculator(instance=calculator_entry)
        calculator_entry_exists = True
    except CalorieCalculatorEntry.DoesNotExist:
        form = CalorieCalculator()
        calculator_entry_exists = False

    if isinstance(selected_date, str):
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None
    if not selected_date:
        selected_date = timezone.now().date()

    print(f"DEBUG: selected_date={selected_date}")

    calorie_entries = CalorieIntakeEntry.objects.filter(user=user, date=selected_date)
    searched_food_items = SearchedFoodItem.objects.filter(user=user, date=selected_date)

    total_calories = (
        sum(entry.calculated_calories for entry in calorie_entries) + 
        sum(item.total_calories for item in searched_food_items)
    )
    total_protein = (
        sum(entry.calculated_protein for entry in calorie_entries) + 
        sum(item.total_protein for item in searched_food_items)
    )

    # calculate calorie and protein target and percentage
    calorie_target = request.session.get('calorie_target')
    protein_target = request.session.get('protein_target')

    calorie_target = Decimal(calorie_target) if calorie_target else None
    protein_target = Decimal(protein_target) if protein_target else None

    calorie_percentage = (
        min((Decimal(total_calories) / calorie_target) * 100, 100) 
        if calorie_target else 0
    )
    protein_percentage = (
        min((Decimal(total_protein) / protein_target) * 100, 100) 
        if protein_target else 0
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
        'form': form,
        'calorie_percentage': round(calorie_percentage, 2) if calorie_target else None,
        'protein_percentage': round(protein_percentage, 2) if protein_target else None,
        'calorie_target': Decimal(calorie_target) if calorie_target else None,
        'protein_target': Decimal(protein_target) if protein_target else None,
        'calculator_entry_exists': calculator_entry_exists,
    }

    return render(request, 'calorie/calorie.html', context)




@login_required(login_url="login")
def add_calorie_entry(request):
    user = request.user
    selected_date = request.POST.get("date") or request.GET.get("date")
    if isinstance(selected_date, str):
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None

    # Fallback to today if no date is provided or invalid
    if not selected_date:
        selected_date = timezone.now().date()

    print(f"DEBUG: selected_date (POST or GET) = {selected_date}")
    saved_entries = FoodItem.objects.filter(user=user)
    
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
                        "picture": food.get("foodCategoryImage"),
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
        
        elif request.POST.get("saved_food_name") and request.POST.get("saved_calories_per_gram"):
            saved_food_name = request.POST.get("saved_food_name")
            saved_calories_per_gram = float(request.POST.get("saved_calories_per_gram", 0))
            saved_protein_per_gram = float(request.POST.get("saved_protein_per_gram", 0))
            saved_amount_in_grams = float(request.POST.get("saved_amount_in_grams", 0))
            
            total_saved_calories = saved_calories_per_gram * saved_amount_in_grams
            total_saved_protein = saved_protein_per_gram * saved_amount_in_grams
            
            SearchedFoodItem.objects.create(
                user=user,
                description=saved_food_name,
                total_calories=total_saved_calories,
                total_protein=total_saved_protein,
                date=selected_date,
            )
            
            return redirect(redirect_url)

        else:
            form = AddCalorieEntryForm(request.POST)
            if form.is_valid():
                food_name = form.cleaned_data["food_name"]
                amount_in_grams = form.cleaned_data["amount_in_grams"]
                calories_per_gram = form.cleaned_data["calories_per_gram"]
                protein_per_gram = form.cleaned_data["protein_per_gram"]

            food_item = FoodItem.objects.filter(name=food_name, user=user).first()

            # Check if the item exists for the current user
            if food_item:
                food_item.calories_per_gram = calories_per_gram
                food_item.protein_per_gram = protein_per_gram
                food_item.save()
            else:
                # Create a new item for the current user
                food_item = FoodItem.objects.create(
                    name=food_name,
                    user=user,
                    calories_per_gram=calories_per_gram,
                    protein_per_gram=protein_per_gram,
                    is_custom=True
                )


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
        'saved_entries': saved_entries,
    }

    return render(request, "calorie/add_entry.html", context)


@login_required(login_url="login")
def delete_calorie_entry(request, entry_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])  # Allow only POST requests

    selected_date = request.POST.get('date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    # Attempt to delete from CalorieIntakeEntry
    entry = CalorieIntakeEntry.objects.filter(id=entry_id, user=request.user).first()
    if entry:
        entry.delete()
    else:
        # Attempt to delete from SearchedFoodItem
        searched_entry = SearchedFoodItem.objects.filter(id=entry_id, user=request.user).first()
        if searched_entry:
            searched_entry.delete()
        else:
            # Attempt to delete from FoodItem (Saved Entries)
            food_item = FoodItem.objects.filter(id=entry_id, user=request.user).first()
            if food_item:
                food_item.delete()
            else:
                # If the entry doesn't exist in any table, raise a 404 error
                raise Http404("Entry not found.")

    redirect_to = request.POST.get("redirect_to", "calorieTracker:calorie_tracker")
    return redirect(f"{reverse(redirect_to)}?date={selected_date}")


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

def calculate_bmi_calories(request):
    if request.method == "POST":
        form = CalorieCalculator(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = int(form.cleaned_data['age'])
            biological_sex = form.cleaned_data['biological_sex']
            body_fat_percentage = form.cleaned_data.get('body_fat_percentage')
            activity_level = form.cleaned_data['activity_level']
            goal_weight = form.cleaned_data['goal_weight']

            # Perform BMI Calculation
            bmi = weight / ((height / Decimal(100)) ** 2)

            # Perform BMR (Mifflin-St Jeor Equation)
            if biological_sex == 'male':
                bmr = Decimal(10) * weight + Decimal(6.25) * height - Decimal(5) * age + Decimal(5)
            else:
                bmr = Decimal(10) * weight + Decimal(6.25) * height - Decimal(5) * age - Decimal(161)

            # TDEE calculation
            activity_multiplier = {
                'sedentary': Decimal('1.2'),
                'light': Decimal('1.375'),
                'moderate': Decimal('1.55'),
                'very_active': Decimal('1.725'),
                'super_active': Decimal('1.9')
            }
            tdee = bmr * activity_multiplier[activity_level]

            # Adjust for goal weight
            calorie_target = tdee - Decimal(500) if weight > goal_weight else tdee + Decimal(500)

            # Check if an entry exists for the user
            calorie_entry, created = CalorieCalculatorEntry.objects.update_or_create(
                user=request.user,
                defaults={
                    "weight": weight,
                    "height": height,
                    "age": age,
                    "biological_sex": biological_sex,
                    "body_fat_percentage": body_fat_percentage,
                    "activity_level": activity_level,
                    "goal_weight": goal_weight,
                    "bmi": bmi,
                    "bmr": bmr,
                    "tdee": tdee,
                    "calorie_target": calorie_target,
                }
            )

            # Update session data
            request.session['bmi'] = round(float(bmi), 2)
            request.session['calorie_target'] = round(float(calorie_target), 2)
            request.session['protein_target'] = round(float(weight * Decimal('1.6')), 2)

            return redirect('calorieTracker:calorie_tracker')

    else:
        form = CalorieCalculator()

    return render(request, 'calorie/calorie.html', {'form': form})


@login_required(login_url="login")
def edit_calculator(request):
    user_entry = get_object_or_404(CalorieCalculatorEntry, user=request.user)

    if request.method == "POST":
        form = CalorieCalculator(request.POST, instance=user_entry)
        if form.is_valid():
            updated_entry = form.save()
            request.session['calorie_target'] = round(float(updated_entry.calorie_target), 2)
            request.session['protein_target'] = round(float(updated_entry.weight * Decimal('1.6')), 2)
            return redirect('calorieTracker:calorie_tracker')
    else:
        form = CalorieCalculator(instance=user_entry)

    return render(request, "calorie/calorie.html", {"form": form})
