"""
API views for authentication and user management.
"""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers.user import UserSerializer


class UserProfileView(APIView):
    """API endpoint for retrieve and update user profile."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return the authenticated user's profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update the authenticated user's profile."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
