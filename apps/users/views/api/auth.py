"""
API views for authentication (register and login) with optional 2FA.
"""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers.auth import LoginSerializer, RegisterSerializer
from apps.users.serializers.user import UserSerializer


class RegisterView(APIView):
    """API endpoint for user registration."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle user registration and return user data."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "User registered. Please log in.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """API endpoint for user login with optional 2FA."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle user login and initiate 2FA if enabled."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if user.use_2fa:
                # Store user email in session for OTP verification
                request.session["pending_user_email"] = user.email
                return Response(
                    {"message": "OTP sent to your email.", "user_email": user.email},
                    status=status.HTTP_200_OK,
                )
            else:
                # Issue tokens directly if 2FA is disabled
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": UserSerializer(user).data,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
