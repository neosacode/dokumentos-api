from apps.documents.serializers import DocumentsSerializer
from apps.documents.models import Document
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.documents.permissions import IsOwnerOrReadOnly


class DocumentsList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    # queryset = Document.objects.all()
    serializer_class = DocumentsSerializer

    def get_queryset(self):
        queryset = Document.objects.filter(user=self.request.user)
        return queryset


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Document.objects.all()
    
    serializer_class = DocumentsSerializer
