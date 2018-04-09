from rest_framework import serializers
from apps.documents.models import Document, Model


class ModelWithUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # when create a document get the currently autenticated user
        request = self.context['request']
        model = self.Meta.model
        return model.objects.create(user=request.user, **validated_data)


class DocumentSerializer(ModelWithUserSerializer):
    class Meta:
        model = Document
        fields = ('ref', 'type', 'country', 'model', 'file', 'status', 'webhook')


class CreateDocumentSerializer(DocumentSerializer):
    country = serializers.CharField()
    type = serializers.CharField()
    model = serializers.CharField()

    def validate(self, data):
        kwargs = dict(type__abbr=data['type'], country__abbr=data['country'], abbr=data['model'])
        model_qs = Model.objects.filter(**kwargs)
        if not model_qs.exists():
            raise serializers.ValidationError("Country/Type don't match with Model")
        self.model = model_qs.first()
        return super().validate(data)

    class Meta:
        model = Document
        fields = ('type', 'country', 'model', 'webhook')
