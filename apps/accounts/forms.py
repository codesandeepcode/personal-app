from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
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
    username = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist.")
        
        return cleaned_data
