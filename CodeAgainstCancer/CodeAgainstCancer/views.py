import json
import logging
import os
import random
import time

import requests
from accounts.models import UserProfile, Donor
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from accounts.forms import DonorForm
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qsl, urlencode

#from pyexpat.errors import messages

from .api_handlers import APIHandlerFactory
from .forms import ContactForm
from .utils import LoggerSingleton, cache_results

# Create a logger instance
logger = LoggerSingleton()


def single_error_message(request, message_text): #makes sure a specific error message is only showed once
    """Ensure a unique error message is added only once."""
    if message_text not in [msg.message for msg in get_messages(request)]:
        messages.error(request, message_text)

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
    form = AuthenticationForm(request, data=request.POST or None)
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
                messages.warning(request, "Please complete your profile information.")
                return redirect("update_profile")

            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


@login_required(login_url="login")
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
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Generate query based on user profile or default query
    if user_profile.cancer_type and user_profile.cancer_stage:
        query = f"{user_profile.cancer_type} cancer {user_profile.cancer_stage} stage"
    else:
        query = "cancer patients support"

    # Using the ResourceFactory to determine the correct API handler
    youtube_handler = APIHandlerFactory.get_API_handler("video")
    pubmed_handler = APIHandlerFactory.get_API_handler("article")

    # Get the page token from the request if provided
    page_token = request.GET.get("page_token", None)

    # Fetch YouTube videos and PubMed articles using the handlers
    youtube_start = time.time()  # Start timer for YouTube API call
    youtube_videos = youtube_handler.fetch(query, page_token=page_token)
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
    Handle the donation page and render the wall of contributors.
    """

    total_amount = Donor.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch the top 9 donors, ordered by the most recent
    donors = Donor.objects.order_by('-date')[:9]

    # Placeholder data for when there are fewer than 9 donors
    placeholders = [
        {"name": "Anonymous", "amount": 500, "message": "Inspiring message"},
        {"name": "Anonymous", "amount": 300, "message": "Keep up the fight!"},
        {"name": "Anonymous", "amount": 250, "message": "Together we are stronger."},
        {"name": "Anonymous", "amount": 450, "message": "Supporting this cause."},
        {"name": "Anonymous", "amount": 700, "message": "Proud to be a donor."},
        {"name": "Anonymous", "amount": 350, "message": "Every bit counts."},
        {"name": "Anonymous", "amount": 600, "message": "Making a difference."},
        {"name": "Anonymous", "amount": 800, "message": "Thank you for your work!"},
        {"name": "Anonymous", "amount": 1000, "message": "Keep up the great work."},
    ]

    # Combine real donors and placeholders
    real_donors_dicts = [
        {"name": donor.name or "Anonymous", "amount": donor.amount, "message": donor.message or ""}
        for donor in donors
    ]
    donors = real_donors_dicts + placeholders[len(real_donors_dicts):]

    # Debugging: Check what is being passed to the template
    print(f"Donors passed to template: {donors}")

    return render(request, 'donate/donate.html', {'donors': donors, 'total_amount': total_amount})

def donate_form(request, donor_id=None):
    """
    Handles the donor form submission and redirects appropriately based on user action.
    """

    if donor_id:
        # Fetch the donor object using the donor_id
        donor = get_object_or_404(Donor, id=donor_id)
    else:
        # Create a new donor object with a placeholder amount and default fields
        donor = Donor.objects.create(amount=0.0)
        # Redirect to the same view with the newly created donor_id
        return redirect('donate_form', donor_id=donor.id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "leave_message":
            # Save the name and message fields to the donor object
            form = DonorForm(request.POST, instance=donor)
            if form.is_valid():
                form.save()
        # Redirect to the donor wall regardless of the action
        return redirect('donate_wall')  # Assuming this is the name for the contributor wall

    else:
        # Initialize the form with the existing donor instance
        form = DonorForm(instance=donor)

    return render(request, 'donate/donate_form.html', {'form': form, 'donor': donor})


logger = logging.getLogger(__name__)

def paypal_ipn_listener(request):
    if request.method == 'POST':
        try:
            # Capture raw IPN data as bytes
            raw_ipn_data = request.body  # bytes
            logger.info(f"Raw IPN data received (bytes): {raw_ipn_data}")

            # Prepend 'cmd=_notify-validate' as bytes
            verify_data = b'cmd=_notify-validate&' + raw_ipn_data
            logger.info(f"Data sent for verification (bytes): {verify_data}")

            # Send data back to PayPal for verification
            verify_url = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'close',
            }
            response = requests.post(verify_url, data=verify_data, headers=headers, timeout=30)
            logger.info(f"PayPal verification response status: {response.status_code}")
            logger.info(f"PayPal verification response text: '{response.text}'")

            # Handle PayPal's response
            if response.text.strip() == "VERIFIED":
                logger.info("IPN verified successfully.")
                # Proceed with processing
                return HttpResponse("VERIFIED", status=200)
            else:
                logger.warning("Invalid IPN")
                return HttpResponse("INVALID", status=200)
        except Exception as e:
            logger.error(f"Error processing IPN: {e}")
            return HttpResponse("Error", status=200)
    else:
        logger.warning("Non-POST request received at IPN listener.")
        return HttpResponse("Method Not Allowed", status=405)




# @cache_results(timeout=300)
@login_required(login_url="login")
def searchRecipes(request):
    user = request.user
    query = request.GET.get("query", "")
    page = int(request.GET.get("page", 1))
    from_recipes = (page - 1) * 6
    to_recipes = page * 6
    recipes = []
    excluded_query = ""


    user_profile = get_object_or_404(UserProfile, user=user)
    json_path = os.path.join(settings.BASE_DIR, "static/cancer_information.json")
    with open(json_path, "r") as json_file:
        cancer_data = json.load(json_file)

    cancer_info = cancer_data.get(user_profile.cancer_type, {})
    excluded_ingredients = cancer_info.get("excluded_ingredients", [])
    dietary_retrictions = cancer_info.get("dietary_restrictions", "")
    recommended_foods = cancer_info.get("recommended_foods", "")
    special_instructions = cancer_info.get("special_instructions", "")
    
    if any(excluded in query for excluded in excluded_ingredients):
        # Set an error message and skip the API call
        single_error_message(request, "Your query includes an ingredient you should avoid. Please try again without it.")
        context = {
            "recipes": recipes,
            "query": query,
            "page": page,
            "hasNextPage": False,
            "hasPrevPage": False,
            "excluded_ingredients": excluded_ingredients,
            "dietary_restrictions": dietary_retrictions,
            "recommended_foods": recommended_foods,
            "special_instructions": special_instructions,
        }
        return render(request, "recipe/recipe.html", context)
    
    
    excluded_query = "&".join([f"excluded={ingredient}" for ingredient in excluded_ingredients])
    if not query:
        random_offset = random.randint(0, 1000)
        url = f"https://api.edamam.com/search?q=recipe&app_id={settings.APP_ID}&app_key={settings.API_KEY}&from={random_offset}&to={random_offset + 6}&{excluded_query}"
    else:
        url = f"https://api.edamam.com/search?q={query}&app_id={settings.APP_ID}&app_key={settings.API_KEY}&from={from_recipes}&to={to_recipes}&{excluded_query}"

    context = {
        "recipes": recipes,
        "query": query,
        "page": page,
        "hasNextPage": False,  # Default values for error handling
        "hasPrevPage": False,
        "excluded_ingredients": excluded_ingredients,
        "dietary_restrictions": dietary_retrictions,
        "recommended_foods": recommended_foods,
        "special_instructions": special_instructions,
    }

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            recipes = data.get("hits", [])
            total_recipes = data.get("count", 0)
            hasNextPage = to_recipes < total_recipes
            hasPrevPage = from_recipes > 0

            context.update({
                "recipes": recipes,
                "hasNextPage": hasNextPage,
                "hasPrevPage": hasPrevPage,
            })
        else:
            single_error_message(request, "Unable to fetch recipes at this time. Please try again later")
            logger.error(f"API request failed with a status code {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        single_error_message(request, "Unable to fetch recipes at this time due to network issues")
        
        
    return render(request, "recipe/recipe.html", context)



def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            content = form.cleaned_data["content"]

            html = render_to_string(
                "emails/email.html", {"name": name, "email": email, "content": content}
            )
            # Send the email using Django's send_mail function
            send_mail(
                "Contact Form Submission",
                "This is the message from the contact form.",  # You might want to include the content here as well
                settings.DEFAULT_FROM_EMAIL,  # Use the configured default from email
                ["codeagainstcancer@outlook.com"],
                html_message=html,
                fail_silently=False,
            )
            return redirect("contact")  # Redirect back to the contact page
    else:
        form = ContactForm()  # Initialize an empty form

    # Render the contact form with context
    return render(request, "contact/contactform.html", {"form": form})
