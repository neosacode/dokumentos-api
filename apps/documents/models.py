import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel
from apps.documents.choices import STATUS_CHOICES
from apps.core.models import BaseModel

user_model = settings.AUTH_USER_MODEL


class Country(BaseModel):
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countrys')


class Type(BaseModel):
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')


class Model(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='models')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        unique_together = (("country", "type", "abbr"),)


class Document(TimeStampedModel, BaseModel):
    ref = models.CharField(max_length=300)
    error = models.CharField(max_length=300, null=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    file = models.URLField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name=_("status"), default=STATUS_CHOICES.pending)
    user = models.ForeignKey(user_model, related_name='user', on_delete=models.CASCADE)
    webhook = models.URLField()
    tries = models.IntegerField(default=0)
    request_id = models.UUIDField(default=uuid.uuid4, null=True)
    is_ready = models.BooleanField(default=False)
    contains = JSONField(default={})
    has_contains = models.BooleanField(default=False)
    ocr = models.TextField(null=True)

    def __str__(self):
        return '{} | {} - {} - {}'.format(self.user.username, self.model.country.name, self.model.type.name, self.model.name)

    def set_ocr_text(self, text):
        self.ocr = text
        self.save()

    def send_to_recognition(self):
        self.has_contains = True
        self.save()

    def increment_tries(self, error):
        self.error = error
        self.tries += 1
        self.save()

    def send_to_validation(self, contains):
        self.error = None
        self.tries = 0
        self.is_ready = True
        self.contains = contains
        self.save()

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class Requests(BaseModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = JSONField()
