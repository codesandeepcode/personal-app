"""
Tests for session-based UI views (auth, dashboard, and OTP) using fixtures with optional 2FA.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models.user import User
from apps.users.models.otp import OTP
from django.utils import timezone
from django.core import mail

@pytest.mark.django_db
class SessionViewTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

    def test_login_view_get(self):
        """Test rendering login page with Bootstrap."""
        response = self.client.get(reverse('login'))
        assert response.status_code == 200
        assert 'users/login.html' in [t.name for t in response.templates]
        assert 'bootstrap.min.css' in response.content.decode()
        assert 'needs-validation' in response.content.decode()

    def test_login_view_post_2fa_enabled(self):
        """Test successful session-based login with 2FA enabled."""
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'securepassword123'
        })
        assert response.status_code == 302
        assert response.url == reverse('otp_verify')
        assert self.client.session['pending_user_id']
        assert len(mail.outbox) == 1
        assert 'Your one-time password is' in mail.outbox[0].body

    def test_login_view_post_2fa_disabled(self):
        """Test successful session-based login with 2FA disabled."""
        response = self.client.post(reverse('login'), {
            'email': 'admin@example.com',
            'password': 'adminpassword123'
        })
        assert response.status_code == 302
        assert response.url == reverse('dashboard')
        assert self.client.session['_auth_user_id']
        assert len(mail.outbox) == 0

    def test_login_view_post_invalid(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200
        assert 'Invalid credentials' in response.content.decode()
        assert 'alert-danger' in response.content.decode()

    def test_otp_verify_view_success(self):
        """Test successful OTP verification."""
        user = User.objects.get(email='test@example.com')
        self.client.force_login(user)
        self.client.session['pending_user_id'] = user.id
        self.client.session.save()
        OTP.objects.create(
            user=user,
            code='123456',
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            is_used=False
        )
        response = self.client.post(reverse('otp_verify'), {'code': '123456'})
        assert response.status_code == 302
        assert response.url == reverse('dashboard')
        assert self.client.session['_auth_user_id']
        assert OTP.objects.get(code='123456').is_used

    def test_otp_verify_view_invalid(self):
        """Test invalid OTP verification."""
        user = User.objects.get(email='test@example.com')
        self.client.force_login(user)
        self.client.session['pending_user_id'] = user.id
        self.client.session.save()
        response = self.client.post(reverse('otp_verify'), {'code': '999999'})
        assert response.status_code == 200
        assert 'Invalid OTP' in response.content.decode()

    def test_dashboard_view_authenticated(self):
        """Test dashboard access for authenticated user with fixture data."""
        self.client.login(email='admin@example.com', password='adminpassword123')
        response = self.client.get(reverse('dashboard'))
        assert response.status_code == 200
        assert 'users/dashboard.html' in [t.name for t in response.templates]
        assert 'bootstrap.min.css' in response.content.decode()
        assert 'list-group' in response.content.decode()

    def test_dashboard_view_unauthenticated(self):
        """Test dashboard access for unauthenticated user."""
        response = self.client.get(reverse('dashboard'))
        assert response.status_code == 302
        assert response.url == '/login/?next=/dashboard/'

    def test_logout_view(self):
        """Test logout redirects to login page."""
        self.client.login(email='admin@example.com', password='adminpassword123')
        response = self.client.get(reverse('logout'))
        assert response.status_code == 302
        assert response.url == reverse('login')
        assert '_auth_user_id' not in self.client.session
        