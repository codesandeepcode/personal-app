"""
Session-based views for UI dashboard
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    """Render the user dashboard."""
    return render(request, 'accounts/dashboard.html', {'user': request.user})
