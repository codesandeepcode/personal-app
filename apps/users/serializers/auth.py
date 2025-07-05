"""
Serializer for authentication (registration and login).
"""
from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.users.models.user import User
from apps.users.models.otp import OTP
from django.core.mail import send_mail


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    name = serializers.CharField(max_length=100, required=True, allow_blank=False)
    use_2fa = serializers.BooleanField(default=False)

    def validate_email(self, value):
        """Check if the email is already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value
    
    def create(self, validated_data):
        """Create a new user with the validated data."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            use_2fa=validated_data.get('use_2fa', False)
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    """Serializer for user login with 2FA."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Validate user credentials and handle 2FA."""
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            if user.use_2fa:
                # Generate OTP for 2FA
                otp = OTP.generate_otp(user)
                # Send OTP via email
                send_mail(
                    subject='Your OTP for Login',
                    message=f'Your one-time password is: {otp.code}\nIt is valid for 5 minutes.',
                    from_email='no-reply@yourdomain.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            return user
        raise serializers.ValidationError("Invalid credentials or inactive account.")
