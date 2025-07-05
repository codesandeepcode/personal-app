"""
Session-based views for UI authentication with optional 2FA.
"""
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from apps.users.models.otp import OTP


def login_view(request):
    """Handle session-based login with optional 2FA."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.use_2fa:
                otp = OTP.generate_otp(user)
                # Send OTP via email
                send_mail(
                    subject='Your OTP for Login',
                    message=f'Your one-time password is: {otp.code}\nIt is valid for 5 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                # Store user ID in session for OTP verification
                request.session['pending_user_email'] = user.email
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
