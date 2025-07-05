"""
Tests for OTPSerializer.
"""
import pytest
from django.test import TestCase
from django.utils import timezone
from apps.users.models.otp import OTP
from apps.users.models.user import User
from apps.users.serializers.otp import OTPSerializer
from rest_framework import serializers

@pytest.mark.django_db
class OTPSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='securepassword123',
            name='Test User'
        )
        self.client.force_login(self.user)

    def test_valid_otp(self):
        """Test valid OTP verification."""
        OTP.objects.create(
            user=self.user,
            code='123456',
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            is_used=False
        )
        serializer = OTPSerializer(data={'code': '123456'}, context={'request': self.client.request()})
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'test@example.com'
        assert OTP.objects.get(code='123456').is_used

    def test_invalid_otp(self):
        """Test invalid OTP."""
        serializer = OTPSerializer(data={'code': '999999'}, context={'request': self.client.request()})
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_expired_otp(self):
        """Test expired OTP."""
        OTP.objects.create(
            user=self.user,
            code='654321',
            created_at=timezone.now(),
            expires_at=timezone.now() - timezone.timedelta(minutes=1),
            is_used=False
        )
        serializer = OTPSerializer(data={'code': '654321'}, context={'request': self.client.request()})
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
