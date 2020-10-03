from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'tages.countries.CountriesConfig'


class CountriesConfig(AppConfig):
    name = 'tages.countries'
    verbose_name = _('Countries')
