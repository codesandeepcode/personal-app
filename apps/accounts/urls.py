"""
URL configuration for user authentication and registration.
"""
from django.urls import path
from apps.accounts.views.ui.auth import login_view, logout_view
from apps.accounts.views.ui.dashboard import dashboard_view
from apps.accounts.views.api.auth import RegisterView, LoginView
from apps.accounts.views.api.profile import UserProfileView

UI = (
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
)

API = (
    path("api/register/", RegisterView.as_view(), name="api_register"),
    path("api/login/", LoginView.as_view(), name="api_login"),
    path("api/profile/", UserProfileView.as_view(), name="api_profile"),
)

urlpatterns = UI + API
