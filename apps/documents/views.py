from apps.documents.serializers import DocumentsSerializer
from apps.documents.models import Documents
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class DocumentsList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
