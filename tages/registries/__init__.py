from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'tages.registries.RegistriesConfig'


class RegistriesConfig(AppConfig):
    name = 'tages.registries'
    verbose_name = _('Registries')
