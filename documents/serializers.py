from rest_framework import serializers
from documents.models import Documents


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
