import requests
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


def user_logout(request):
    logout(request)
    return redirect('home')

def homepageView(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check if the user has completed their profile
            if not (user.profile.cancer_type and user.profile.date_diagnosed and user.profile.cancer_stage and user.profile.gender):
                return redirect('user_profile.html')  # Redirect to profile form if not completed

            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def resources(request):
    query = "cancer patients support"
    data = get_youtube_videos(query)
    videos = data.get("items", [])
    context = { "videos": videos }
    return render(request, 'resources/resources.html', context)

def get_youtube_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 10,
        "order": "relevance",
        "key": settings.YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def about(request):
    return render(request, 'about/about.html')