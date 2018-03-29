import boto3
import uuid
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework import authentication, status
from rest_framework.response import Response
from apps.core import authentication as core_authentication
from apps.documents.serializers import DocumentSerializer, CreateDocumentSerializer
from apps.documents.models import Document


class DocumentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = (authentication.SessionAuthentication, core_authentication.BearerTokenAuthentication,)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        metadata = {'x-amz-meta-{}'.format(k): v for k, v in serializer.data.items()}
        conditions = [{k: v} for k, v in metadata.items()]
        
        s3 = boto3.client('s3')
        presigned = s3.generate_presigned_post(Bucket=settings.S3_BUCKET, Key=uuid.uuid4().hex, Conditions=conditions)
        presigned['fields'].update(metadata)
        
        return Response(presigned, status=status.HTTP_201_CREATED)
