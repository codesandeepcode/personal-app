"""
API view for OTP verification.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers.otp import OTPSerializer
from apps.users.serializers.user import UserSerializer

class OTPVerifyView(APIView):
    """API endpoint for OTP verification."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Verify OTP and issue JWT tokens."""
        serializer = OTPSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
