from django.urls import path
from .views import RegisterView, CustomLoginView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
]