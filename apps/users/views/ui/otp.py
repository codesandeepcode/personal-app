"""
Session-based view for OTP verification.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from apps.users.models.otp import OTP
from apps.users.models.user import User

def otp_verify_view(request):
    """Handle OTP verification for session-based login."""
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user = User.objects.get(email=request.session.get('pending_user_email'))
            otp = OTP.objects.get(user=user, code=code, is_used=False)
            if otp.is_valid():
                otp.is_used = True
                otp.save()
                login(request, user)  # Complete login
                del request.session['pending_user_email']
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP.')
        return render(request, 'users/otp-verify.html', {'error': 'Invalid OTP.'})
    return render(request, 'users/otp-verify.html')
