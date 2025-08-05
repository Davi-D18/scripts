from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.authentication.schemas import UserSerializer, CustomerTokenObtainPairSerializer
from django.contrib.auth import get_user_model


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomerTokenObtainPairSerializer
