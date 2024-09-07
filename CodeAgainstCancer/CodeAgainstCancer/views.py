import requests
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import random
import logging


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

logger = logging.getLogger(__name__)

def searchRecipes(request):
    query = request.GET.get('query', '')  # gets search result from user
    page = int(request.GET.get('page', 1))
    from_recipes = (page - 1) * 6
    to_recipes = page * 6 #this keeps track of up to 6 different recipes per page
    recipes = []

    # load random recipes if no search result is inputted
    if not query:
        logger.debug('No query provided. Fetching random recipes.')
        random_offset = random.randint(0, 1000)  # Adjust range based on total number of recipes available
        url = f'https://api.edamam.com/search?q=recipe&app_id={settings.APP_ID}&app_key={settings.API_KEY}&from={random_offset}&to={random_offset + 6}'
    else:
        # Fetch recipes based on the search query and also using from recipes and to recipes are used to get different recipes in 6 recipes per page
        url = f'https://api.edamam.com/search?q={query}&app_id={settings.APP_ID}&app_key={settings.API_KEY}&from={from_recipes}&to={to_recipes}'

    response = requests.get(url)
    data = response.json()
    recipes = data.get('hits', [])

    total_recipes = data.get('count', 0)
    hasNextPage = to_recipes < total_recipes
    hasPrevPage = from_recipes > 0

    context = {
        'recipes': recipes,
        'query': query,
        'page': page,
        'hasNextPage': hasNextPage,
        'hasPrevPage': hasPrevPage
    }

    return render(request, 'recipe/recipe.html', context)