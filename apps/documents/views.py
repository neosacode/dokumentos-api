import uuid
import boto3

from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework import authentication, status
from rest_framework.response import Response
from munch import DefaultMunch as munch

from apps.core import authentication as core_authentication
from apps.documents.serializers import DocumentSerializer, CreateDocumentSerializer
from apps.documents.models import Document, Requests


class DocumentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = (authentication.SessionAuthentication, core_authentication.BearerTokenAuthentication,)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ref = serializer.validated_data['ref']
        webhook = serializer.validated_data['webhook']
        data = dict(model_id=str(serializer.model.pk), user_id=str(request.user.pk), ref=str(ref), webhook=str(webhook))
        document_request = Requests.objects.create(data=data)
        metadata = {'x-amz-meta-request': str(document_request.pk)}
        conditions = [{k: v} for k, v in metadata.items()]

        s3 = boto3.client('s3')
        presigned = s3.generate_presigned_post(Bucket=settings.S3_BUCKET, Key=uuid.uuid4().hex, Conditions=conditions)
        presigned['fields'].update(metadata)

        return Response(presigned, status=status.HTTP_201_CREATED)
