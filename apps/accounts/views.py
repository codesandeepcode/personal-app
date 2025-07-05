from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from .serializers import UserSerializer
from .forms import CustomAuthenticationForm
from rest_framework.response import Response


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "accounts/login.html"

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)