from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ('email', 'name')

class CustomUserChangeForm(UserChangeForm):
    class Meta():
        model = CustomUser
        fields = ('email', 'name')

class CustomAuthenticationForm(AuthenticationForm):  
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    
    def clean(self):
        super(CustomAuthenticationForm, self).clean()
        email = self.cleaned_data.get('email')
        if email:
            password = self.cleaned_data.get('password')
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid email or password."
                )
        return self.cleaned_data
