from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import thread_list, thread_detail, create_thread, create_post, reply_to_post

urlpatterns = [
    path('forum/', thread_list, name='thread_list'),
    path('forum/thread/<int:pk>/', thread_detail, name='thread_detail'),
    path('forum/thread/new/', create_thread, name='create_thread'),
    path('forum/thread/<int:pk>/post/new/', create_post, name='create_post'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)