import io
import os
import boto3
import requests

from google.cloud import vision
from google.cloud.vision import types

from django.conf import settings
from django.db import transaction
from apps.core.utils import print_message
from apps.documents.models import Document
from apps.ocr.api import VisionApi
from apps.ocr.messages import VALUE_NOT_EXISTS

s3 = boto3.client('s3')


while True:
    documents = Document.objects.filter(is_ready=True, error=None)
    
    for document in documents:
        object_key = document.file.split('/')[-1]
        presigned_params = {'Bucket': settings.S3_BUCKET, 'Key': object_key}
        image_uri = s3.generate_presigned_url('get_object', Params=presigned_params, ExpiresIn=100)

        vision_api = VisionApi(settings.OCR_GOOGLECLOUD_KEY)
        text = vision_api.get_text_from_image_uri(image_uri)

        with transaction.atomic():
            # Stores the text extract from the document
            document.set_ocr_text(text)
            # Copy the dict for no object implicit change
            contains = dict(document.contains)
            words = contains.pop('words')

            # Starts the validation proccess of the contains data
            # If contains has no data to be validated, check the document to go to next validation step
            if not bool(contains) and not bool(words):
                document.send_to_recognition()
                continue

            # Validate the required contains data
            for k, v in contains.items():
                if not v in text:
                    document.increment_tries(print_message(VALUE_NOT_EXISTS.format(v, k)))
                    break

            # Skips to next document if the current document has an error
            if document.error is not None:
                continue

            # Finishs the contains validation by words extra argument
            for w in words:
                if not w in text:
                    document.increment_tries(print_message(VALUE_NOT_EXISTS.format(v, k)))
                    break

            # If everything is ok than the document is sent to the recognition
            document.send_to_recognition()
