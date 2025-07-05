"""
Tests for the OTP model.
"""
import pytest
from django.test import TestCase
from django.utils import timezone
from apps.users.models.otp import OTP
from apps.users.models.user import User

@pytest.mark.django_db
class OTPModelTests(TestCase):
    def test_generate_otp(self):
        """Test OTP generation."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(email=email, password=password, name="Test User")
        otp = OTP.generate_otp(user)
        assert len(otp.code) == 6
        assert otp.user == user
        assert otp.is_valid()
        assert not otp.is_used

    def test_otp_expiry(self):
        """Test OTP expiry validation."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(email=email, password=password, name="Test User")
        otp = OTP.objects.create(
            user=user,
            code='654321',
            created_at=timezone.now(),
            expires_at=timezone.now() - timezone.timedelta(minutes=1),
            is_used=False
        )
        assert not otp.is_valid()

    def test_otp_used(self):
        """Test used OTP is invalid."""
        email = "test@example.com"
        password = "securepassword123"
        user = User.objects.create_user(email=email, password=password, name="Test User")
        otp = OTP.objects.create(
            user=user,
            code='987654',
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            is_used=True
        )
        assert not otp.is_valid()
