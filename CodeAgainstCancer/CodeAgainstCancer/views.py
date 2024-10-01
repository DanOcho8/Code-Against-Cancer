import random
import time

import requests
from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .api_handlers import APIHandlerFactory
from .utils import LoggerSingleton, cache_results

# Create a logger instance
logger = LoggerSingleton()


def user_logout(request):
    """
    Logs out the current user and redirects to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the home page.
    """
    logger.info(f"User {request.user.id} is attempting to log out.")
    logout(request)
    logger.info("User logged out successfully.")
    return redirect("home")


def homepageView(request):
    """
    Renders the homepage view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage HTML.
    """
    return render(request, "home.html")


def login_view(request):
    """
    Handle user login and redirect based on profile completion.

    This view processes the login form submission. If the form is valid and the user is authenticated,
    it checks whether the user has completed their profile. If the profile is incomplete, the user is
    redirected to the profile form page. Otherwise, the user is redirected to the home page.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object with the rendered login page or a redirect to another page.
    """
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


@cache_results(timeout=7200)
def resources(request):
    """
    Handles the resources view which fetches YouTube videos and PubMed articles based on the user's profile.

    This view performs the following steps:
    1. Checks if the user is authenticated. If not, redirects to the login page.
    2. Retrieves the user's profile.
    3. Generates a query based on the user's cancer type and stage, or uses a default query.
    4. Uses the ResourceFactory to get the appropriate API handlers for YouTube and PubMed.
    5. Fetches YouTube videos and PubMed articles using the handlers.
    6. Logs the time taken for each API call.
    7. Prepares the context with the fetched data and pagination tokens.
    8. Returns a JSON response if the request is an AJAX request.
    9. Renders the resources template with the context data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered resources page or a JSON response if it's an AJAX request.
    """
    start_time = time.time()  # Start timer for the view function
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
    youtube_handler = APIHandlerFactory.get_API_handler("video")
    pubmed_handler = APIHandlerFactory.get_API_handler("article")

    # Get the page token from the request for pagination
    page_token = request.GET.get("page_token", None)

    # Fetch YouTube videos and PubMed articles using the handlers
    youtube_start = time.time()  # Start timer for YouTube API call
    youtube_videos = youtube_handler.fetch(query, page_token=page_token)
    # Log the time taken for the YouTube API call
    logger.info(f"YouTube API call took {time.time() - youtube_start:.2f} seconds.")

    pubmed_start = time.time()  # Start timer for PubMed API call
    pubmed_articles = pubmed_handler.fetch(query)
    logger.info(f"PubMed API call took {time.time() - pubmed_start:.2f} seconds.")

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

    total_time = time.time() - start_time  # Calculate total time taken for the view
    logger.info(f"Total resources view response time: {total_time:.2f} seconds.")
    logger.info("Resources successfully fetched and returned.")
    return render(request, "resources/resources.html", context)


def about(request):
    """
    Handles the request for the 'About' page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'About' page.
    """
    return render(request, "about/about.html")


def donate(request):
    """
    Handle the donation page request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered donation page.
    """
    return render(request, "donate/donate.html")


@cache_results(timeout=300)
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
