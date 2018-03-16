from apps.documents.serializers import DocumentSerializer
from apps.documents.models import Document
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)