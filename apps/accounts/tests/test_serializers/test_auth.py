"""
Tests for authentication serializers (RegisterSerializer and LoginSerializer).
"""
import pytest
from django.test import TestCase
from apps.accounts.models.user import User
from apps.accounts.serializers.auth import RegisterSerializer, LoginSerializer
from rest_framework import serializers

@pytest.mark.django_db
class AuthSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123')

    def test_register_serializer_valid(self):
        """Test valid registration data."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'name': 'New User'
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'newuser@example.com'
        assert user.check_password('newpassword123')
        assert user.name == 'New User'

    def test_register_serializer_duplicate_email(self):
        """Test registration with duplicate email."""
        data = {'email': 'test@example.com', 'password': 'newpassword123'}
        serializer = RegisterSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_serializer_valid(self):
        """Test valid login credentials."""
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.validated_data
        assert user.email == 'test@example.com'

    def test_login_serializer_invalid(self):
        """Test invalid login credentials."""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        serializer = LoginSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
