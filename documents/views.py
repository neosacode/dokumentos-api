from documents.serializers import DocumentsSerializer
from documents.models import Documents
from rest_framework import generics


class DocumentsList(generics.ListCreateAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
