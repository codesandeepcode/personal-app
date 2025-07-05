"""
API views for authentication and user management.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.serializers.auth import RegisterSerializer, LoginSerializer
from apps.accounts.serializers.user import UserSerializer


class RegisterView(APIView):
    """API endpoint for user registration."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle user registration and return JWT token."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    """API endpoint for user login."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle user login and return JWT token."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
