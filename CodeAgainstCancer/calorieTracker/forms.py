from django import forms

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
    
class CalorieCalculator(forms.Form):
    weight = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        label="weight",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Weight'})
    )
    height = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        label="height",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Height'})
    )
    age = forms.IntegerField(
    label="Age",
    widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Age'}),
    )
    
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    biological_sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        label="Biological Sex",
        widget=forms.RadioSelect,
    )
    body_fat_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Body Fat Percentage (Optional)",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Body Fat %'}),
    )
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (Little or no exercise)'),
        ('light', 'Lightly Active (Light exercise/sports 1-3 days/week)'),
        ('moderate', 'Moderately Active (Moderate exercise/sports 3-5 days/week)'),
        ('very_active', 'Very Active (Hard exercise/sports 6-7 days/week)'),
        ('super_active', 'Super Active (Very hard exercise/physical job)'),
    ]
    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        label="Activity Level",
        widget=forms.Select,
    )
    
    goal_weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Goal Weight (kg)",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Goal Weight in kg'}),
    )
