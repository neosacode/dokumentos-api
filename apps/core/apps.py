from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'apps.core'
    verbose_name = _('Core')

    def ready(self):
    	import apps.core.signals