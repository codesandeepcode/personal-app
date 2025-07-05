"""
Tests for the custom User model and UserManager using fixtures.
"""

import pytest
from django.test import TestCase
from django.utils import timezone

from apps.users.models.otp import OTP
from apps.users.models.user import User


@pytest.mark.django_db
class UserModelTests(TestCase):
    fixtures = ["users.json"]

    def test_create_user(self):
        """Test creating a user with valid email and password."""
        email = "newuser@example.com"
        password = "newpassword123"
        user = User.objects.create_user(
            email=email, password=password, name="New User", use_2fa=True
        )
        assert user.email == email
        assert user.check_password(password)
        assert user.name == "New User"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.use_2fa

    def test_create_user_no_email(self):
        """Test creating a user without an email raises ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="securepassword123")

    def test_create_superuser(self):
        """Test creating a superuser with valid email and password."""
        email = "newadmin@example.com"
        password = "newadminpassword123"
        user = User.objects.create_superuser(
            email=email, password=password, use_2fa=False
        )
        assert user.email == email
        assert user.check_password(password)
        assert user.is_staff
        assert user.is_superuser
        assert not user.use_2fa

    def test_create_superuser_invalid(self):
        """Test creating a superuser without staff status raises ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="newadmin@example.com",
                password="newadminpassword123",
                is_staff=False,
            )

    def test_fixture_user(self):
        """Test properties of user loaded from fixture."""
        user = User.objects.get(email="test@example.com")
        assert user.email == "test@example.com"
        assert user.check_password("securepassword123")
        assert user.name == "Test User"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.use_2fa

    def test_fixture_superuser(self):
        """Test properties of superuser loaded from fixture."""
        user = User.objects.get(email="admin@example.com")
        assert user.email == "admin@example.com"
        assert user.check_password("adminpassword123")
        assert user.name == "Admin User"
        assert user.is_active
        assert user.is_staff
        assert user.is_superuser
        assert not user.use_2fa


@pytest.mark.django_db
class OTPModelTests(TestCase):
    def test_generate_otp(self):
        """Test OTP generation."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(
            email=email, password=password, name="Test User"
        )
        otp = OTP.generate_otp(user)
        assert len(otp.code) == 6
        assert otp.user == user
        assert otp.is_valid()
        assert not otp.is_used

    def test_otp_expiry(self):
        """Test OTP expiry validation."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(
            email=email, password=password, name="Test User"
        )
        otp = OTP.objects.create(
            user=user,
            code="654321",
            created_at=timezone.now(),
            expires_at=timezone.now() - timezone.timedelta(minutes=1),
            is_used=False,
        )
        assert not otp.is_valid()

    def test_otp_used(self):
        """Test used OTP is invalid."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(
            email=email, password=password, name="Test User"
        )
        otp = OTP.objects.create(
            user=user,
            code="987654",
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            is_used=True,
        )
        assert not otp.is_valid()
