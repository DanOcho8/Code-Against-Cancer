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
    date = forms.DateField(
        widget=forms.SelectDateWidget, 
        label="Date"
    )
