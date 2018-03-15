from rest_framework import serializers
from apps.documents.models import Document


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
