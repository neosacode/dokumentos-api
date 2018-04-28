import sys
import importlib
import requests

from json import JSONDecodeError
from urllib.parse import urljoin

from munch import DefaultMunch as munch
from django.conf import settings
from django.db import transaction
from apps.core.utils import print_message
from apps.documents.models import Requests, Document, Model
from apps.documents.choices import STATUS_CHOICES
from apps.webhook.exceptions import KeyNotInResponseException, WordsListException
from apps.webhook.messages import (DOCUMENT_CREATED_MESSAGE, REQUEST_NOT_FOUND_MESSAGE, 
                                   DOCUMENT_PREPARED_MESSAGE, INVALID_JSON_MESSAGE)

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
        print_message(DOCUMENT_CREATED_MESSAGE.format(document.pk))

    except Requests.DoesNotExist:
        message.delete()
        print_message(REQUEST_NOT_FOUND_MESSAGE.format(meta_request))


def parse_contains_response(validator, contains_response):
    contains = {}
    for key, cast in validator.items():
        if not key in contains_response:
            raise KeyNotInResponseException(key)
        contains[key] = cast(contains_response[key])
    words = contains_response.get('words')
    if words and not isinstance(words, list):
        raise WordsListException()
    return {'words': contains_response.get('words'), **contains}


def fire_webhook(document):
    try:
        data = munch()
        data.request_id = document.request_id
        data.ref = document.ref
        data.country = document.model.country.abbr
        data.type = document.model.type.abbr
        data.model = document.model.abbr

        contains_response = requests.post(document.webhook, data=data.toDict()).json()
        validator_module = importlib.import_module('apps.webhook.validators.{}'.format(data.country.lower()))
        validator_attr_name = '{}_{}_{}'.format(data.country, data.type, data.model)
        validator = getattr(validator_module, validator_attr_name)

        contains = parse_contains_response(validator, contains_response)
        document.send_to_validation(contains)
        print_message(DOCUMENT_PREPARED_MESSAGE.format(document.pk))

    except WordsListException as e:
        document.increment_tries(print_message(e))

    except KeyNotInResponseException as e:
        document.increment_tries(print_message(e))

    except JSONDecodeError as e:
        document.increment_tries(print_message(INVALID_JSON_MESSAGE))
