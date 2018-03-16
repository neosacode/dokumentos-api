from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from apps.core import serializers


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CreateUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.TokenAuthentication,)

    def get_queryset(self):
        return [self.request.user]