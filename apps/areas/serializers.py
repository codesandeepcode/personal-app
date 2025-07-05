"""Areas application serializers for handling API data serialization and validation."""

from .models import Area
from rest_framework import serializers


class AreaSerializer(serializers.ModelSerializer):
    """Serializer for the Area model."""

    class Meta:
        """Meta class for AreaSerializer."""

        model = Area
        fields = ["name", "slug"]
        read_only_fields = ["slug"]
        extra_kwargs = {"name": {"required": True, "allow_blank": False}}

    def validate_name(self, value):
        """Validate the name field to ensure it is not empty."""
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value
