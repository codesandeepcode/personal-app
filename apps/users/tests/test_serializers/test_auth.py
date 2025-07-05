"""
Tests for authentication serializers (RegisterSerializer and LoginSerializer) with optional 2FA.
"""
import pytest
from django.test import TestCase
from django.core import mail
from apps.users.serializers.auth import RegisterSerializer, LoginSerializer
from rest_framework import serializers

@pytest.mark.django_db
class AuthSerializerTests(TestCase):
    fixtures = ['users.json']

    def test_register_serializer_valid(self):
        """Test valid registration data with 2FA option."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'use_2fa': True
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'newuser@example.com'
        assert user.check_password('newpassword123')
        assert user.first_name == 'New'
        assert user.use_2fa

    def test_register_serializer_duplicate_email(self):
        """Test registration with duplicate email from fixture."""
        data = {'email': 'test@example.com', 'password': 'newpassword123'}
        serializer = RegisterSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_serializer_valid_2fa_enabled(self):
        """Test valid login with 2FA enabled from fixture."""
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        serializer = LoginSerializer(data=data, context={'request': self.client.request()})
        assert serializer.is_valid()
        user = serializer.validated_data
        assert user.email == 'test@example.com'
        assert len(mail.outbox) == 1
        assert 'Your one-time password is' in mail.outbox[0].body

    def test_login_serializer_valid_2fa_disabled(self):
        """Test valid login with 2FA disabled from fixture."""
        data = {'email': 'admin@example.com', 'password': 'adminpassword123'}
        serializer = LoginSerializer(data=data, context={'request': self.client.request()})
        assert serializer.is_valid()
        user = serializer.validated_data
        assert user.email == 'admin@example.com'
        assert len(mail.outbox) == 0  # No OTP email sent

    def test_login_serializer_invalid(self):
        """Test invalid login credentials."""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        serializer = LoginSerializer(data=data, context={'request': self.client.request()})
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
