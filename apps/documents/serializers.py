from rest_framework import serializers
from apps.documents.models import Document


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
