# CodeAgainstCancer/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import contact

urlpatterns = [
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('calorieTracker/', include('calorieTracker.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.homepageView , name="home"),
    path("logout", views.user_logout , name='logout'),
    path('accounts/', include('allauth.urls')),
    path('resources/', views.resources, name='resources'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('about/', views.about, name='about'),
    path('recipes/', views.searchRecipes, name='searchRecipes'),
    path('donate/', views.donate, name='donate'),
    path('donate/donate_form/', views.donate_form, name='donate_form'),
    path('contact/', contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy')
    # Add more URL patterns as needed
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
