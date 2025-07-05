"""
Tests for UserSerializer.
"""
import pytest
from django.test import TestCase
from apps.accounts.models.user import User
from apps.accounts.serializers.user import UserSerializer

@pytest.mark.django_db
class UserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='securepassword123',
            name='Test User'
        )

    def test_user_serializer_read(self):
        """Test serializing user data."""
        serializer = UserSerializer(self.user)
        data = serializer.data
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'
        assert 'id' in data
        assert 'date_joined' in data

    def test_user_serializer_update(self):
        """Test updating user data."""
        data = {'name': 'Updated Name'}
        serializer = UserSerializer(self.user, data=data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.name == 'Updated Name'
