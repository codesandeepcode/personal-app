"""
Tests for API views (auth and profile).
"""
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models.user import User


@pytest.mark.django_db
class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123', name="Test User")

    def test_register_view(self):
        """Test user registration API."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'name': 'New User'
        }
        response = self.client.post('/accounts/api/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == 'newuser@example.com'
        assert response.data['user']['name'] == 'New User'

    def test_register_view_invalid(self):
        """Test registration with existing email."""
        data = {'email': 'test@example.com', 'password': 'securepassword123', "name": "Test User"}
        response = self.client.post('/accounts/api/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_view(self):
        """Test user login API."""
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        response = self.client.post('/accounts/api/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == 'test@example.com'
        assert response.data['user']['name'] == 'Test User'

    def test_login_view_invalid(self):
        """Test login with invalid credentials."""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/accounts/api/login/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_view_get(self):
        """Test retrieving user profile."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/accounts/api/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'test@example.com'
        assert response.data['name'] == 'Test User'

    def test_profile_view_put(self):
        """Test updating user profile."""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Name'}
        response = self.client.put('/accounts/api/profile/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Name'
