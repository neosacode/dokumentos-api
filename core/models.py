from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Users(TimeStampedModel, AbstractUser, BaseModel):

    default_webhook = models.URLField()
    default_pending_message = models.TextField()
    default_valid_message = models.TextField()
    default_invalid_message = models.TextField()
