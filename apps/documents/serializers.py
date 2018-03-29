from rest_framework import serializers
from apps.documents.models import Document, Country, Type, Model


class ModelWithUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # when create a document get the currently autenticated user
        request = self.context['request']
        model = self.Meta.model
        return model.objects.create(user=request.user, **validated_data)


class DocumentSerializer(ModelWithUserSerializer):
    # overwrite for can user str fields
    country = serializers.SlugRelatedField(slug_field='abbr', queryset=Country.objects.all())
    type = serializers.SlugRelatedField(slug_field='abbr', queryset=Type.objects.all())
    model = serializers.SlugRelatedField(slug_field='abbr', queryset=Model.objects.all())
    
    class Meta:
        model = Document
        fields = ('type', 'country', 'model', 'file', 'status', 'webhook')
        extra_kwargs = {'status': {'required': False}, 'file': {'required': False}}


class CreateDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Document
        fields = ('type', 'country', 'model', 'webhook')