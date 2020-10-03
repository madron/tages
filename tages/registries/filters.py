from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class BaseActiveFilter(admin.SimpleListFilter):
    title = _('active')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            (None, _('Yes')),
            ('no', _('No')),
            ('all', _('All')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


class RegistryActiveFilter(BaseActiveFilter):
    def queryset(self, request, queryset):
        value = self.value()
        if value == 'no':
            return queryset.filter(deactivation_date__isnull=False)
        if value == 'all':
            return queryset
        return queryset.filter(deactivation_date__isnull=True)
