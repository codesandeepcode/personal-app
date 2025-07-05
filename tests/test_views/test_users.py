"""
Tests for API and session-based UI views (auth, dashboard, and OTP) using fixtures with optional 2FA.
"""
import pytest

from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models.otp import OTP
from apps.users.models.user import User


@pytest.mark.django_db
class APITests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = APIClient()

    def test_register_view(self):
        """Test user registration API with 2FA option."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'name': 'New User',
            'use_2fa': True
        }
        response = self.client.post('/users/api/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['email'] == 'newuser@example.com'
        assert response.data['user']['use_2fa'] is True

    def test_register_view_invalid(self):
        """Test registration with existing email from fixture."""
        data = {'email': 'test@example.com', 'password': 'newpassword123'}
        response = self.client.post('/users/api/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_view_2fa_enabled(self):
        """Test user login API with 2FA enabled."""
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        response = self.client.post('/users/api/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'OTP.sent to your email.'
        assert 'user_id' in response.data
        assert len(mail.outbox) == 1
        assert 'Your one-time password is' in mail.outbox[0].body

    def test_login_view_2fa_disabled(self):
        """Test user login API with 2FA disabled."""
        data = {'email': 'admin@example.com', 'password': 'adminpassword123'}
        response = self.client.post('/users/api/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == 'admin@example.com'
        assert len(mail.outbox) == 0

    def test_login_view_invalid(self):
        """Test login with invalid credentials."""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/users/api/login/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_otp_verify_view(self):
        """Test OTP verification API."""
        user = User.objects.get(email='test@example.com')
        self.client.force_authenticate(user=user)
        OTP.objects.create(
            user=user,
            code='123456',
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            is_used=False
        )
        response = self.client.post('/users/api/otp/verify/', {'code': '123456'}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert OTP.objects.get(code='123456').is_used

    def test_profile_view_get(self):
        """Test retrieving user profile from fixture."""
        user = User.objects.get(email='test@example.com')
        self.client.force_authenticate(user=user)
        response = self.client.get('/users/api/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'test@example.com'
        assert response.data['use_2fa'] is True

    def test_profile_view_put(self):
        """Test updating user profile from fixture."""
        user = User.objects.get(email='test@example.com')
        self.client.force_authenticate(user=user)
        data = {'name': 'Updated User', 'use_2fa': False}
        response = self.client.put('/users/api/profile/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated User'
        assert response.data['use_2fa'] is False


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
        assert self.client.session['pending_user_email'] == 'test@example.com'
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
        self.client.session['pending_user_email'] = user.email
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
        self.client.session['pending_user_email'] = user.email
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
        assert response.url == '/users/login/?next=/users/dashboard/'

    def test_logout_view(self):
        """Test logout redirects to login page."""
        self.client.login(email='admin@example.com', password='adminpassword123')
        response = self.client.get(reverse('logout'))
        assert response.status_code == 302
        assert response.url == reverse('login')
        assert '_auth_user_id' not in self.client.session
        