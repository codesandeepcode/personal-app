from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .serializers import UserSerializer
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from rest_framework.response import Response


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return Response(form.errors, status=400)
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/signup.html", {"form": form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)