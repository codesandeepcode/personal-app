"""
Model for storing One-Time Passwords (OTPs) for 2FA.
"""
import secrets
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .user import User

class OTP(models.Model):
    """Model to store OTPs for two-factor authentication."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTPs')

    def __str__(self):
        return f"OTP {self.code} for {self.user.email}"

    @classmethod
    def generate_otp(cls, user):
        """Generate a new OTP for the user."""
        code = ''.join(secrets.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(6))
        expires_at = timezone.now() + timezone.timedelta(minutes=5)
        return cls.objects.create(user=user, code=code, expires_at=expires_at)

    def is_valid(self):
        """Check if the OTP is valid (not used and not expired)."""
        return not self.is_used and timezone.now() <= self.expires_at