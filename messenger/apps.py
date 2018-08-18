from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MessengerConfig(AppConfig):
    name = 'messenger'
    verbose_name = _('Messager')