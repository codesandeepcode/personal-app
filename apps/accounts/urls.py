from django.urls import path
from .views import RegisterView, CustomLoginView, signup, CustomLogoutView

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
]