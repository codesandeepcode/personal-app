"""
Serializer for the User model
"""
from rest_framework import serializers
from apps.users.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ["id", "email", "name", "is_active", "use_2fa", "date_joined"]
        read_only_fields = ["id", "date_joined"]
