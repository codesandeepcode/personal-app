"""
URL configuration for user authentication and registration.
"""
from django.urls import path
from apps.users.views.ui.auth import login_view, logout_view
from apps.users.views.ui.dashboard import dashboard_view
from apps.users.views.ui.otp import otp_verify_view
from apps.users.views.api.auth import RegisterView, LoginView
from apps.users.views.api.profile import UserProfileView
from apps.users.views.api.otp import OTPVerifyView

UI = (
    path('login/', login_view, name='login'),
    path('otp/verify/', otp_verify_view, name='otp_verify'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
)

API = (
    path("api/register/", RegisterView.as_view(), name="api_register"),
    path("api/login/", LoginView.as_view(), name="api_login"),
    path("api/otp/verify/", OTPVerifyView.as_view(), name="api_otp_verify"),
    path("api/profile/", UserProfileView.as_view(), name="api_profile"),
)

urlpatterns = UI + API
