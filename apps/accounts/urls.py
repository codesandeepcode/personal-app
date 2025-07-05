"""
URL configuration for user authentication and registration.
"""
from django.urls import path
from . import views, api_views

urlpatterns = [
    path("api/register/", api_views.RegisterView.as_view(), name="api_register"),
    path("api/login/", api_views.LoginView.as_view(), name="api_login"),
    path("api/profile/", api_views.UserProfileView.as_view(), name="api_profile"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
]