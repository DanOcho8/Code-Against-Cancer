# CodeAgainstCancer/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepageView , name="home"),
    path("logout", views.user_logout , name='logout'),
    path('accounts/', include('allauth.urls')),
    path('resources/', views.resources, name='resources'),
    path('about/', views.about, name='about'),
    path('recipe/', views.recipe, name='recipe'),
    # Add more URL patterns as needed
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
