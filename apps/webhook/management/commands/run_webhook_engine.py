import json
import time

import boto3
import gevent

from datetime import datetime
from django.conf import settings
from munch import DefaultMunch as munch


from apps.documents.models import Document
from apps.webhook.task import create_document, fire_webhook



MAXIMUM_STACK_SIZE = settings.WEBHOOK_MAXIMUM_STACK_SIZE
MAXIMUM_TRIES = settings.WEBHOOK_MAXIMUM_TRIES
QUEUE_NAME = settings.WEBHOOK_QUEUE_NAME

sqs = boto3.resource('sqs')
s3 = boto3.client('s3')

queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

stack = []
stack_size = 0


while True:
	for message in queue.receive_messages(MaxNumberOfMessages=10):
		body = munch.fromDict(json.loads(message.body))

		for record in body.Records:
			stack.append(munch(bucket=record.s3.bucket.name, key=record.s3.object.key))

	previous_stack_size = stack_size
	stack_size = len(stack)

	if previous_stack_size != stack_size and stack_size < MAXIMUM_STACK_SIZE:
		continue	

	# Process SQS document messages
	gevent.wait([gevent.spawn(create_document, s3, message, i.bucket, i.key) for i in stack[:MAXIMUM_STACK_SIZE]])

	# Process documents who should be webhooked
	documents_qs = Document.objects.filter(tries__lt=MAXIMUM_TRIES, is_ready=False)
	gevent.wait([gevent.spawn(fire_webhook, document) for document in documents_qs[:MAXIMUM_STACK_SIZE]])

	if stack_size == 0:
		time.sleep(5)

	# Erase stack for a new greenlet batch generation
	stack[:] = []
