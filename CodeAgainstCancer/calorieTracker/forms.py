from django import forms
from .models import CalorieCalculatorEntry

class AddCalorieEntryForm(forms.Form):
    food_name = forms.CharField(
        max_length=100, 
        label="Food Name", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter food item'})
    )
    amount_in_grams = forms.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        label="Amount in Grams", 
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount in grams'})
    )
    calories_per_gram = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Calories per Gram",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter calories per gram'})
    )
    protein_per_gram = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Protein per Gram",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter protein per gram'})
    )
    
from django import forms

class CalorieCalculator(forms.ModelForm):
    class Meta:
        model = CalorieCalculatorEntry
        fields = [
            'weight',
            'height',
            'age',
            'biological_sex',
            'body_fat_percentage',
            'activity_level',
            'goal_weight',
        ]

    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Weight (kg)",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Weight in kg'}),
    )
    height = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Height (cm)",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Height in cm'}),
    )
    age = forms.IntegerField(
        label="Age",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Age'}),
    )
    biological_sex = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.RadioSelect,
        label="Biological Sex",
    )
    body_fat_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Body Fat Percentage (Optional)",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Body Fat %'}),
    )
    activity_level = forms.ChoiceField(
        choices=[
            ('sedentary', 'Sedentary (Little or no exercise)'),
            ('light', 'Lightly Active (Light exercise/sports 1-3 days/week)'),
            ('moderate', 'Moderately Active (Moderate exercise/sports 3-5 days/week)'),
            ('very_active', 'Very Active (Hard exercise/sports 6-7 days/week)'),
            ('super_active', 'Super Active (Very hard exercise/physical job)'),
        ],
        label="Activity Level",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    goal_weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Goal Weight (kg)",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Goal Weight in kg'}),
    )