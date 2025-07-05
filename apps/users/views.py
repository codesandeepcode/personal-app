"""
session-based views for authentication and user management using UI.
"""
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login_view(request):
    """Handle session-based user login for UI."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'users/login.html')


@login_required
def dashboard_view(request):
    """Render the user dashboard."""
    return render(request, 'users/dashboard.html', {'user': request.user})


@login_required
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('login')
