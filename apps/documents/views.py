import boto3
import uuid
from rest_framework import viewsets, mixins
from rest_framework import authentication, status
from rest_framework.response import Response
from apps.core import authentication as core_authentication
from apps.documents.serializers import DocumentSerializer
from apps.documents.models import Document


class DocumentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = (authentication.SessionAuthentication, core_authentication.BearerTokenAuthentication,)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        s3 = boto3.client('s3')
        conditions = [{'Metadata': {'userid': str(request.user.pk.hex)}}]
        presigned = s3.generate_presigned_post(Bucket='dokumentos-dev', Key=uuid.uuid4().hex, Conditions=conditions)

        for k, v in serializer.data.items():
            if k not in ['type', 'country', 'model']:
                continue
            meta_name = 'x-amz-meta-{}'.format(k)
            presigned['fields'][meta_name] = v

        return Response(presigned, status=status.HTTP_201_CREATED)
