from rest_framework import viewsets
from rest_framework import authentication
from apps.core import serializers, authentication as core_authentication
from apps.documents.serializers import DocumentSerializer
from apps.documents.models import Document


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = (authentication.SessionAuthentication, core_authentication.BearerTokenAuthentication,)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
