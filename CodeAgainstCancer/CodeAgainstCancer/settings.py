"""
This settings file includes configurations for:
- Base directory setup
- Environment variable loading
- Security settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- API keys
- Installed applications
- Authentication backends and social account providers
- Email backend configuration
- Middleware
- URL configuration
- Templates
- WSGI application
- Database configuration
- Password validation
- Internationalization
- Static and media files
- Default primary key field type
- User authentication and redirection
- Security settings (CSRF, session cookies, SSL, HSTS)
- Content Security Policy (CSP)
Django settings for CodeAgainstCancer project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# API keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "django_google_fonts",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_extensions",
    "widget_tweaks",
    "phonenumber_field",
    "tests",
    "csp",
    'forum',
    'mathfilters',
    'calorieTracker',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {"access_type": "online", "OAUTH_PKCE_ENABLED": True},
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = os.getenv(
    "SENDGRID_API_KEY"
)  # Ensure the password is stored securely
DEFAULT_FROM_EMAIL = "codeagainstcancer@outlook.com"
EMAIL_FROM = "codeagainstcancer@outlook.com"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "forum.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "CodeAgainstCancer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "CodeAgainstCancer.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "static/",
]
GOOGLE_FONTS = ["Montserrat"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "auth.User"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# Security settings
CSRF_COOKIE_SECURE = not DEBUG  # Ensures the CSRF cookie is only sent over HTTPS (production only).
CSRF_COOKIE_SAMESITE = "Lax"  # Restricts CSRF cookie from being sent with cross-site requests, except for top-level navigations.
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG # Ensures session cookies are only sent over HTTPS, protecting them from being exposed over HTTP.
SECURE_BROWSER_XSS_FILTER = True  # Enables the browser's built-in XSS filter to help prevent cross-site scripting (XSS) attacks.
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents the browser from guessing (sniffing) the MIME type, reducing the risk of security vulnerabilities.
SECURE_SSL_REDIRECT = not DEBUG # Redirects all HTTP requests to HTTPS when not in DEBUG mode (production only).
X_FRAME_OPTIONS = "DENY"  # Prevents the site from being displayed in an iframe, mitigating clickjacking attacks.
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents the browser from guessing (sniffing) the MIME type, reducing the risk of security vulnerabilities.

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0 # Enforces HTTPS by telling browsers to only use HTTPS for the next 1 year (or 0 in development).
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG # Ensures HSTS is applied to all subdomains in production.
SECURE_HSTS_PRELOAD = not DEBUG # Allows your site to be included in browsers' HSTS preload lists (used in production).
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents the browser from guessing (sniffing) the MIME type, reducing the risk of security vulnerabilities.

# Content Security Policy (CSP) (if using django-csp)
CSP_DEFAULT_SRC = ("'none'",)
CSP_STYLE_SRC = (
    "'self'",  # Allow styles from the same origin
    "'unsafe-inline'",  # TODO: we should remove this and also remove inline styles
    "https://fonts.googleapis.com",  # Google Fonts
    "https://cdn.jsdelivr.net",  # Bootstrap
    "https://cdnjs.cloudflare.com",  # Font Awesome
)
CSP_SCRIPT_SRC = (
    "'self'",  # Allow scripts from the same origin
    "https://cdn.jsdelivr.net",  # Bootstrap scripts (if any in the future)
    "'unsafe-inline'",  # TODO: we should remove this and also remove inline scripts
)
CSP_FONT_SRC = (
    "'self'",  # Fonts from the same origin
    "https://fonts.gstatic.com",  # Google Fonts
    "https://cdnjs.cloudflare.com",  # Font Awesome
)
CSP_IMG_SRC = (
    "'self'",
    "*",
    "data:",
)  # Allow images from the same origin, any external domain, and data: URIs
CSP_CONNECT_SRC = ("'self'",)  # Only allow connections from your Django app (for APIs)
CSP_FRAME_SRC = (
    "'self'",
    "https://www.youtube.com",  # Allow iframes from YouTube
)
CSP_BASE_URI = ("'self'",)  # Allow base tag to refer to your Django app
CSP_OBJECT_SRC = ("'none'",)  # Block plugins like Flash (outdated, but good practice)
