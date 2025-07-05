"""
Session-based view for OTP verification.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils import timezone
from django.contrib import messages
from apps.users.models.otp import OTP

def otp_verify_view(request):
    """Handle OTP verification for session-based login."""
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            otp = OTP.objects.get(user=request.user, code=code, is_used=False)
            if otp.is_valid():
                otp.is_used = True
                otp.save()
                login(request, request.user)  # Complete login
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP.')
        return render(request, 'users/otp-verify.html', {'error': 'Invalid OTP.'})
    return render(request, 'users/otp-verify.html')
