from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from CodeAgainstCancer import views
from CodeAgainstCancer.views import contact


class TestUrls(SimpleTestCase):
    """
    TestUrls is a test case class that contains unit tests for the URL patterns in the application.
    """

    def test_home_url_is_resolved(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, views.homepageView)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, views.user_logout)

    def test_resources_url_is_resolved(self):
        url = reverse("resources")
        self.assertEqual(resolve(url).func, views.resources)

    def test_password_reset_url_is_resolved(self):
        url = reverse("password_reset")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url_is_resolved(self):
        url = reverse("password_reset_done")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url_is_resolved(self):
        url = reverse(
            "password_reset_confirm",
            kwargs={"uidb64": "test-uidb64", "token": "test-token"},
        )
        self.assertEqual(
            resolve(url).func.view_class, auth_views.PasswordResetConfirmView
        )

    def test_password_reset_complete_url_is_resolved(self):
        url = reverse("password_reset_complete")
        self.assertEqual(
            resolve(url).func.view_class, auth_views.PasswordResetCompleteView
        )

    def test_about_url_is_resolved(self):
        url = reverse("about")
        self.assertEqual(resolve(url).func, views.about)

    def test_search_recipes_url_is_resolved(self):
        url = reverse("searchRecipes")
        self.assertEqual(resolve(url).func, views.searchRecipes)

    def test_donate_url_is_resolved(self):
        url = reverse("donate")
        self.assertEqual(resolve(url).func, views.donate)

    def test_contact_url_is_resolved(self):
        url = reverse("contact")
        self.assertEqual(resolve(url).func, contact)
