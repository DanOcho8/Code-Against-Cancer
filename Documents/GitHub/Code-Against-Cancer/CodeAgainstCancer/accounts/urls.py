# accounts/urls.py
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import signup, profile_view, update_profile


urlpatterns = [
    path('registration/', signup, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
] + static(settings.STATIC_URL) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
