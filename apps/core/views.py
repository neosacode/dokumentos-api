from rest_framework import viewsets, mixins, authentication, permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from apps.core import serializers, authentication as core_authentication


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CreateUserSerializer


class UserViewSet(mixins.RetrieveModelMixin, 
				  mixins.UpdateModelMixin, 
				  mixins.ListModelMixin, 
				  viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.SessionAuthentication, core_authentication.BearerTokenAuthentication,)

    def get_queryset(self):
        return [self.request.user]