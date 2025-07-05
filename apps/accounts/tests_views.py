"""
Tests for API and session-based views.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')

    def test_register_view_invalid(self):
        """Test registration with existing email."""
        data = {'email': 'test@example.com', 'password': 'securepassword123', "name": "Test User"}
        response = self.client.post('/accounts/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view(self):
        """Test user login API."""
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        response = self.client.post('/accounts/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_view_invalid(self):
        """Test login with invalid credentials."""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/accounts/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_view(self):
        """Test retrieving user profile."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/accounts/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

@pytest.mark.django_db
class SessionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123')

    def test_login_view_get(self):
        """Test rendering login page."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'bootstrap.min.css')  # Check for Bootstrap CSS
        self.assertContains(response, 'needs-validation')  # Check for Bootstrap form validation

    def test_login_view_post_success(self):
        """Test successful session-based login."""
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'securepassword123'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_view_post_invalid(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')
        self.assertContains(response, 'alert-danger')  # Check for Bootstrap alert

    def test_dashboard_view_authenticated(self):
        """Test dashboard access for authenticated user."""
        self.client.login(email='test@example.com', password='securepassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
        self.assertContains(response, 'bootstrap.min.css')  # Check for Bootstrap CSS
        self.assertContains(response, 'list-group')  # Check for Bootstrap list group

    def test_dashboard_view_unauthenticated(self):
        """Test dashboard access for unauthenticated user."""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/dashboard/')