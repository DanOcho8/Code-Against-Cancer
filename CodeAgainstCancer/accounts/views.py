import json
import os
from django.conf import settings
from .forms import CustomUserCreationForm, UpdateUserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django import forms   
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import CANCER_TYPE_CHOICES
from django.utils import timezone
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful!"))
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    cancer_type_display = dict(CANCER_TYPE_CHOICES).get(user_profile.cancer_type, user_profile.cancer_type)

    json_path = os.path.join(settings.BASE_DIR, 'static/cancer_information.json')
    with open(json_path, 'r') as json_file:
        cancer_data = json.load(json_file)
    cancer_info = cancer_data.get(user_profile.cancer_type, {
        'dietary_restrictions': 'No specific restrictions.',
        'recommended_foods': 'General healthy diet recommendations.',
        'special_instructions': 'Follow general health advice.'
    })

    context = {
        'user': user,
        'user_profile': user_profile,
        'cancer_type_display': cancer_type_display,
        'cancer_info': cancer_info
    }
    return render(request, 'profile/profile_page.html', context)

def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            backend = request.session.get('_auth_user_backend')
            login(request, current_user, backend=backend)
            messages.success(request, ("Your profile has been updated!"))
            return redirect('home')
        return render(request, 'profile/update_profile.html', {'user_form':user_form})
    else:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home')  