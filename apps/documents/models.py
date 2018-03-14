from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from apps.documents.choices import STATUS_CHOICES
from django.conf import settings
from apps.core.models import BaseModel

user_model = settings.AUTH_USER_MODEL


class Type(BaseModel):
    name = models.CharField(max_length=100)
    abbs = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('type')


class Model(BaseModel):
    name = models.CharField(max_length=100)
    abbs = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('model')


class Country(BaseModel):
    name = models.CharField(max_length=100)
    abbs = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('country')


class Documents(TimeStampedModel, BaseModel):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    file = models.URLField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name=_("status"))
    user = models.ForeignKey(user_model, related_name='user', on_delete=models.CASCADE)
    webhook = models.URLField()

    class Meta:
        verbose_name = _('document')
