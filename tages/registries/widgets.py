from django.forms import Textarea
from tages.utils.widgets import AutocompleteSelect
from . import models


class RegistrySelect(AutocompleteSelect):
    model = models.Registry


class RegistryCustomerSelect(AutocompleteSelect):
    model = models.Registry
    url_name = 'admin:{app_label}_{model_name}_autocomplete_customer'


class RegistrySupplierSelect(AutocompleteSelect):
    model = models.Registry
    url_name = 'admin:{app_label}_{model_name}_autocomplete_supplier'
