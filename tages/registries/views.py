from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from tages.utils.autocomplete import AutocompleteJsonView
from . import models


class RegistryAutocompleteView(PermissionRequiredMixin, AutocompleteJsonView):
    permission_required = 'registries.change_registry'

    def get_queryset(self):
        qs = models.Registry.objects.all()
        if self.term:
            qs = qs.filter(description__icontains=self.term)
        return qs


class RegistryCustomerAutocompleteView(RegistryAutocompleteView):
    def get_queryset(self):
        qs = super(RegistryCustomerAutocompleteView, self).get_queryset()
        return qs.filter(customer=True)


class RegistrySupplierAutocompleteView(RegistryAutocompleteView):
    def get_queryset(self):
        qs = super(RegistrySupplierAutocompleteView, self).get_queryset()
        return qs.filter(supplier=True)
