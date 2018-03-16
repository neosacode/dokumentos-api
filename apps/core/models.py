from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(TimeStampedModel, AbstractUser, BaseModel):
    default_webhook = models.URLField()
    default_pending_message = models.TextField()
    default_valid_message = models.TextField()
    default_invalid_message = models.TextField()

    def save(self, *args, **kwargs):
        """
         Use to hash user password
        """
        self.set_password(self.password)

        return super(User, self).save()

    class Meta:
            verbose_name = _('User')
            verbose_name_plural = _('Users')
