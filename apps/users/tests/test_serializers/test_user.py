"""
Tests for UserSerializer using fixtures with 2FA option.
"""
import pytest
from django.test import TestCase
from apps.users.models.user import User
from apps.users.serializers.user import UserSerializer

@pytest.mark.django_db
class UserSerializerTests(TestCase):
    fixtures = ['users.json']

    def test_user_serializer_read(self):
        """Test serializing user data from fixture."""
        user = User.objects.get(email='test@example.com')
        serializer = UserSerializer(user)
        data = serializer.data
        assert data['email'] == 'test@example.com'
        assert data['first_name'] == 'Test'
        assert data['last_name'] == 'User'
        assert data['use_2fa'] is True
        assert 'id' in data
        assert 'date_joined' in data

    def test_user_serializer_update(self):
        """Test updating user data including 2FA from fixture."""
        user = User.objects.get(email='test@example.com')
        data = {'first_name': 'Updated', 'last_name': 'Name', 'use_2fa': False}
        serializer = UserSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.first_name == 'Updated'
        assert updated_user.last_name == 'Name'
        assert updated_user.use_2fa is False
