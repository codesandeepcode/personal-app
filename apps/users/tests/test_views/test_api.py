"""
Tests for API views (auth, profile, and OTP) using fixtures with optional 2FA.
"""
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models.user import User
from apps.users.models.otp import OTP
from django.utils import timezone
from django.core import mail

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
            'first_name': 'New',
            'last_name': 'User',
            'use_2fa': True
        }
        response = self.client.post('/api/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['email'] == 'newuser@example.com'
        assert response.data['user']['use_2fa'] is True

    def test_register_view_invalid(self):
        """Test registration with existing email from fixture."""
        data = {'email': 'test@example.com', 'password': 'newpassword123'}
        response = self.client.post('/api/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_view_2fa_enabled(self):
        """Test user login API with 2FA enabled."""
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        response = self.client.post('/api/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'OTP.sent to your email.'
        assert 'user_id' in response.data
        assert len(mail.outbox) == 1
        assert 'Your one-time password is' in mail.outbox[0].body

    def test_login_view_2fa_disabled(self):
        """Test user login API with 2FA disabled."""
        data = {'email': 'admin@example.com', 'password': 'adminpassword123'}
        response = self.client.post('/api/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == 'admin@example.com'
        assert len(mail.outbox) == 0

    def test_login_view_invalid(self):
        """Test login with invalid credentials."""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/api/login/', data, format='json')
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
        response = self.client.post('/api/otp/verify/', {'code': '123456'}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert OTP.objects.get(code='123456').is_used

    def test_profile_view_get(self):
        """Test retrieving user profile from fixture."""
        user = User.objects.get(email='test@example.com')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'test@example.com'
        assert response.data['use_2fa'] is True

    def test_profile_view_put(self):
        """Test updating user profile from fixture."""
        user = User.objects.get(email='test@example.com')
        self.client.force_authenticate(user=user)
        data = {'first_name': 'Updated', 'use_2fa': False}
        response = self.client.put('/api/profile/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['use_2fa'] is False
