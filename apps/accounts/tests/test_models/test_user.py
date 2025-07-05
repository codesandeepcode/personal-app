"""
Tests for the custom user model and its manager.
"""
import pytest
from django.test import TestCase
from apps.accounts.models.user import User


@pytest.mark.django_db
class UserModelTests(TestCase):
    def test_create_user(self):
        """Test creating a user with valid email and password."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(email=email, password=password, name="Test User")
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, "Test User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email(self):
        """Test creating a user without an email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="securepassword123")

    def test_create_superuser(self):
        """Test creating a superuser with valid email and password."""
        email = "admin@example.com"
        password = "adminpassword123"
        user = User.objects.create_superuser(email=email, password=password, name="Admin User")
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, "Admin User")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_invalid(self):
        """Test creating a superuser with is_staff=False raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="admin@example.com", password="adminpassword123", is_staff=False)
