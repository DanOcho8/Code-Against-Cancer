import requests
from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


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

    # Get the page token from the request if provided
    page_token = request.GET.get("page_token", None)

    # Fetch YouTube videos based on the query and page token
    data = get_youtube_videos(query, page_token)
    videos = data.get("items", [])
    next_page_token = data.get("nextPageToken", None)
    prev_page_token = data.get("prevPageToken", None)

    # Pass the videos and pagination tokens to the context
    context = {
        "videos": videos,
        "next_page_token": next_page_token,
        "prev_page_token": prev_page_token,
    }

    # Check if it's an AJAX request to return a JSON response
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(context)
    return render(request, "resources/resources.html", context)


def get_youtube_videos(query, page_token=None):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 5,
        "order": "relevance",
        "key": settings.YOUTUBE_API_KEY,
        "videoEmbeddable": "true",
        "type": "video",
    }

    if page_token:
        params["pageToken"] = page_token  # Add the page token for pagination

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching YouTube data: {e}")
        return {"items": []}


def about(request):
    return render(request, "about/about.html")
