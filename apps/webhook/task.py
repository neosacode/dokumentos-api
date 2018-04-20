import sys
import importlib
import requests

from json import JSONDecodeError
from urllib.parse import urljoin

from munch import DefaultMunch as munch
from django.conf import settings
from django.db import transaction
from apps.documents.models import Requests, Document, Model
from apps.documents.choices import STATUS_CHOICES
from apps.documents.exceptions import KeyNotInResponseException

S3_BASEURL = 'https://s3.amazonaws.com'


def create_document(s3, message, bucket, key):
    try:
        head = munch.fromDict(s3.head_object(Bucket=bucket, Key=key))
        meta_request = head.ResponseMetadata.HTTPHeaders['x-amz-meta-request']
        document_request = Requests.objects.get(pk=meta_request)

        with transaction.atomic():
            file = '/'.join([S3_BASEURL, settings.S3_BUCKET, key])
            kwargs = document_request.data
            document = Document.objects.create(**kwargs, file=file, request_id=document_request.pk)
            document_request.delete()
        
        message.delete()
        print('Document {} created based on {}'.format(str(document.pk), kwargs))
    except Requests.DoesNotExist:
        message.delete()
        print('Request {} not found for create a new document'.format(meta_request))


def fire_webhook(document):
    try:
        data = munch()
        data.request_id = str(document.request_id)
        data.ref = document.ref
        data.country = document.model.country.abbr
        data.type = document.model.type.abbr
        data.model = document.model.abbr

        webhook_response = requests.post(document.webhook, data=data.toDict()).json()
        validator_module = importlib.import_module('apps.webhook.validators.{}'.format(data.country.lower()))
        validator_attr_name = '{}_{}_{}'.format(data.country, data.type, data.model)
        validator = getattr(validator_module, validator_attr_name)

        for key, cast in validator.items():
            if not key in webhook_response:
                raise KeyNotInResponseException(key)
            document.contains[key] = cast(webhook_response[key])
        
        document.contains['words'] = webhook_response.get('words')
        document.is_ready = True
        document.save()

        print('Document "{}" has been prepared to be validated'.format(str(document)))

    except KeyNotInResponseException as e:
        document.increment_tries(str(e))
    except JSONDecodeError as e:
        document.increment_tries('Response returned an invalid JSON')