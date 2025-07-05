"""
Serializer for OTP verification.
"""

from rest_framework import serializers

from apps.users.models.otp import OTP


class OTPSerializer(serializers.Serializer):
    """Serializer for OTP verification."""

    code = serializers.CharField(max_length=6, required=True)

    def validate_code(self, value):
        """Validate the OTP code."""
        user = self.context["request"].user
        otp = OTP.objects.get(user=user, code=value, is_used=False)
        if not otp.is_valid():
            raise serializers.ValidationError("OTP is expired or invalid.")
        return value

    def save(self):
        """Mark OTP as used and return the user."""
        user = self.context["request"].user
        otp = OTP.objects.get(user=user, code=self.validated_data["code"])
        otp.is_used = True
        otp.save()
        return user
