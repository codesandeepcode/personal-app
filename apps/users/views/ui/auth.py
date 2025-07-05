"""
Session-based views for UI authentication with optional 2FA.
"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    """Handle session-based login with optional 2FA."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.use_2fa:
                # Store user ID in session for OTP verification
                request.session['pending_user_id'] = user.id
                # Generate OTP (done in LoginSerializer for consistency)
                return redirect('otp_verify')
            else:
                # Complete login if 2FA is disabled
                login(request, user)
                return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def logout_view(request):
    """Handle user logout."""
    request.session.flush()  # Clear session data
    return redirect('login')
