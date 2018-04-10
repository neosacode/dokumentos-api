import sys
from urllib.parse import urljoin

from munch import DefaultMunch as munch
from django.conf import settings
from django.db import transaction
from apps.documents.models import Requests, Document, Model
from apps.documents.choices import STATUS_CHOICES

S3_BASEURL = 'https://s3.amazonaws.com'


def fire_webhook(s3, message, bucket, key):
    head = munch.fromDict(s3.head_object(Bucket=bucket, Key=key))
    metadata = head.ResponseMetadata.HTTPHeaders

    try:
        meta_request = metadata['x-amz-meta-request']
        document_request = Requests.objects.get(pk=meta_request)

        with transaction.atomic():
            file = '/'.join([S3_BASEURL, settings.S3_BUCKET, key])
            request_id = document_request.pk
            kwargs = document_request.data
            document = Document.objects.create(**kwargs, file=file, request_id=request_id)
            document_request.delete()
        
        message.delete()
        print('Document {} created based on {}'.format(str(document.pk), kwargs))
    except Requests.DoesNotExist:
        message.delete()
        print('Request {} not found for create a new document'.format(meta_request))

