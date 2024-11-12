from django.urls import include, path
from .import views

app_name = "calorieTracker"

urlpatterns = [
    path('calorie/', views.calorie_tracker, name='calorie_tracker'),  # Main calorie tracker page
    path('add/', views.add_calorie_entry, name='add_calorie_entry'),  # Add a new calorie entry
    path('delete/<int:entry_id>/', views.delete_calorie_entry, name='delete_calorie_entry'),  # Delete a specific entry
    path('edit/<int:entry_id>/', views.edit_calorie_entry, name='edit_calorie_entry'),  # Edit a specific entry
]