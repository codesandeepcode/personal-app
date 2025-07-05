"""
Tests for UserSerializer using fixtures with 2FA option.
"""

import pytest
from django.core import mail
from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers

from apps.users.models.otp import OTP
from apps.users.models.user import User
from apps.users.serializers.auth import LoginSerializer, RegisterSerializer
from apps.users.serializers.otp import OTPSerializer
from apps.users.serializers.user import UserSerializer


@pytest.mark.django_db
class UserSerializerTests(TestCase):
    fixtures = ["users.json"]

    def test_user_serializer_read(self):
        """Test serializing user data from fixture."""
        user = User.objects.get(email="test@example.com")
        serializer = UserSerializer(user)
        data = serializer.data
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["use_2fa"] is True
        assert "id" in data
        assert "date_joined" in data

    def test_user_serializer_update(self):
        """Test updating user data including 2FA from fixture."""
        user = User.objects.get(email="test@example.com")
        data = {"name": "Updated Name", "use_2fa": False}
        serializer = UserSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.name == "Updated Name"
        assert updated_user.use_2fa is False


@pytest.mark.django_db
class OTPSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="securepassword123", name="Test User"
        )
        self.client.force_login(self.user)

    def test_valid_otp(self):
        """Test valid OTP verification."""
        OTP.objects.create(
            user=self.user,
            code="123456",
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            is_used=False,
        )
        serializer = OTPSerializer(
            data={"code": "123456"}, context={"request": self.client.request()}
        )
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == "test@example.com"
        assert OTP.objects.get(code="123456").is_used

    def test_invalid_otp(self):
        """Test invalid OTP."""
        serializer = OTPSerializer(
            data={"code": "999999"}, context={"request": self.client.request()}
        )
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_expired_otp(self):
        """Test expired OTP."""
        OTP.objects.create(
            user=self.user,
            code="654321",
            created_at=timezone.now(),
            expires_at=timezone.now() - timezone.timedelta(minutes=1),
            is_used=False,
        )
        serializer = OTPSerializer(
            data={"code": "654321"}, context={"request": self.client.request()}
        )
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class AuthSerializerTests(TestCase):
    fixtures = ["users.json"]

    def test_register_serializer_valid(self):
        """Test valid registration data with 2FA option."""
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "name": "New User",
            "use_2fa": True,
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == "newuser@example.com"
        assert user.check_password("newpassword123")
        assert user.name == "New User"
        assert user.use_2fa

    def test_register_serializer_duplicate_email(self):
        """Test registration with duplicate email from fixture."""
        data = {"email": "test@example.com", "password": "newpassword123"}
        serializer = RegisterSerializer(data=data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_login_serializer_valid_2fa_enabled(self):
        """Test valid login with 2FA enabled from fixture."""
        data = {"email": "test@example.com", "password": "securepassword123"}
        serializer = LoginSerializer(
            data=data, context={"request": self.client.request()}
        )
        assert serializer.is_valid()
        user = serializer.validated_data
        assert user.email == "test@example.com"
        assert len(mail.outbox) == 1
        assert "Your one-time password is" in mail.outbox[0].body

    def test_login_serializer_valid_2fa_disabled(self):
        """Test valid login with 2FA disabled from fixture."""
        data = {"email": "admin@example.com", "password": "adminpassword123"}
        serializer = LoginSerializer(
            data=data, context={"request": self.client.request()}
        )
        assert serializer.is_valid()
        user = serializer.validated_data
        assert user.email == "admin@example.com"
        assert len(mail.outbox) == 0  # No OTP email sent

    def test_login_serializer_invalid(self):
        """Test invalid login credentials."""
        data = {"email": "test@example.com", "password": "wrongpassword"}
        serializer = LoginSerializer(
            data=data, context={"request": self.client.request()}
        )
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
