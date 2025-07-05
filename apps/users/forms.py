from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from apps.users.models.user import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "name")


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        if email:
            password = self.cleaned_data.get("password")
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
        return self.cleaned_data
