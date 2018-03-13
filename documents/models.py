from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django.conf import settings
from core.models import BaseModel

Users = settings.AUTH_USER_MODEL


class Type(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Model(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Documents(TimeStampedModel, BaseModel):

    STATUS_CHOICES = Choices('pending', 'valid', 'invalid')
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    file = models.URLField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name=_("status"))
    user = models.ForeignKey(Users, related_name='user', on_delete=models.CASCADE)
    webhook = models.URLField()
