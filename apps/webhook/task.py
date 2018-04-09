from munch import DefaultMunch as munch
from django.conf import settings
from apps.documents.models import Requests, Document, Model
from apps.documents.choices import STATUS_CHOICES


def fire_webhook(s3, bucket, key):
    head = munch.fromDict(s3.head_object(Bucket=bucket, Key=key))
    metadata = head.ResponseMetadata.HTTPHeaders
    document_request = Requests.objects.get(pk=metadata['x-amz-meta-request'])
    document_data = document_request.data

    document = Document()
    document.file = 'https://s3.amazonaws.com/{}/{}'.format(settings.S3_BUCKET, key)
    document.model_id = document_data['model']
    document.user_id = document_data['user']
    document.status = STATUS_CHOICES.pending
    document.save()
    print(document.pk)
