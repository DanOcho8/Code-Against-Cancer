import random

import requests
from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .api_handlers import ResourceFactory
from .utils import LoggerSingleton

logger = LoggerSingleton()


def user_logout(request):
    logout(request)
    return redirect("home")


def homepageView(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check if the user has completed their profile
            if not (
                user.profile.cancer_type
                and user.profile.date_diagnosed
                and user.profile.cancer_stage
                and user.profile.gender
            ):
                return redirect(
                    "user_profile.html"
                )  # Redirect to profile form if not completed

            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def resources(request):
    user = request.user
    # check if user is logged in
    if not user.is_authenticated:
        return redirect("login")

    user_profile = get_object_or_404(UserProfile, user=user)

    # generate query based on user profile or default query
    if user_profile.cancer_type and user_profile.cancer_stage:
        query = f"{user_profile.cancer_type} cancer {user_profile.cancer_stage} stage"
    else:
        query = "cancer patients support"

    # Using the ResourceFactory to determine the correct API handler
    youtube_handler = ResourceFactory.get_resource_handler("video")
    pubmed_handler = ResourceFactory.get_resource_handler("article")

    # Get the page token from the request for pagination
    page_token = request.GET.get("page_token", None)

    # Fetch YouTube videos and PubMed articles using the handlers
    youtube_videos = youtube_handler.fetch(query, page_token=page_token)
    pubmed_articles = pubmed_handler.fetch(query)

    # Fetch pagination tokens from YouTube
    videos = youtube_videos.get("items", [])
    next_page_token = youtube_videos.get("nextPageToken", None)
    prev_page_token = youtube_videos.get("prevPageToken", None)

    context = {
        "videos": videos,
        "next_page_token": next_page_token,
        "prev_page_token": prev_page_token,
        "pubmed_articles": pubmed_articles,
    }

    # Check if it's an AJAX request to return a JSON response
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(context)

    logger.info("Resources successfully fetched and returned.")
    return render(request, "resources/resources.html", context)


def about(request):
    return render(request, "about/about.html")


def donate(request):
    return render(request, "donate/donate.html")


def searchRecipes(request):
    user = request.user
    # check if user is logged in
    if not user.is_authenticated:
        return redirect("login")

    query = request.GET.get("query", "")  # gets search result from user
    page = int(request.GET.get("page", 1))
    from_recipes = (page - 1) * 6
    to_recipes = page * 6  # this keeps track of up to 6 different recipes per page
    recipes = []

    # load random recipes if no search result is inputted
    if not query:
        logger.debug("No query provided. Fetching random recipes.")
        random_offset = random.randint(
            0, 1000
        )  # Adjust range based on total number of recipes available
        url = f"https://api.edamam.com/search?q=recipe&app_id={settings.APP_ID}&app_key={settings.API_KEY}&from={random_offset}&to={random_offset + 6}"
    else:
        # Fetch recipes based on the search query and also using from recipes and to recipes are used to get different recipes in 6 recipes per page
        url = f"https://api.edamam.com/search?q={query}&app_id={settings.APP_ID}&app_key={settings.API_KEY}&from={from_recipes}&to={to_recipes}"

    response = requests.get(url)
    data = response.json()
    recipes = data.get("hits", [])

    total_recipes = data.get("count", 0)
    hasNextPage = to_recipes < total_recipes
    hasPrevPage = from_recipes > 0

    context = {
        "recipes": recipes,
        "query": query,
        "page": page,
        "hasNextPage": hasNextPage,
        "hasPrevPage": hasPrevPage,
    }

    return render(request, "recipe/recipe.html", context)
