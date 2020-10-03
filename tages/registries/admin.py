from django.conf.urls import url
from django.contrib import admin
from django.utils.translation import ugettext as _
from import_export.admin import ExportActionModelAdmin
from reversion.admin import VersionAdmin
from tages.utils.resources import TranslatedModelResource
from . import filters
from . import forms
from . import models
from . import views


ADDRESS_FIELDS = [
    ('province', 'city'),
    ('address', 'street_number'),
    ('zip_code', 'country',),
]
CONTACT_FIELDS = [
    ('phone_number', 'fax_number'),
    ('email', 'pec'),
]


class RegistryResource(TranslatedModelResource):
    class Meta:
        model = models.Registry
        fields = [
            'id', 'last_name', 'first_name', 'social_security_number',
            'alias', 'external_id', 'insert_date', 'deactivation_date',
        ]


@admin.register(models.Registry)
class RegistryAdmin(VersionAdmin, ExportActionModelAdmin):
    list_display = ('get_id', 'description', 'social_security_number', 'active', 'insert_date')
    list_display_links = ('description',)
    list_filter = (filters.RegistryActiveFilter,)
    search_fields = ('description', 'id', 'social_security_number')
    form = forms.RegistryForm
    resource_class = RegistryResource
    fieldsets = [
        (None, {
            'fields': [
                ('last_name', 'first_name',),
                ('social_security_number', 'deactivation_date',),
            ]
        }),
        (_('Address'), {
            'fields': ADDRESS_FIELDS,
        }),
        (_('Contacts'), {
            'fields': CONTACT_FIELDS,
        }),
    ]

    def get_urls(self):
        info = dict(app_label=self.model._meta.app_label, model_name=self.model._meta.model_name)
        urls = [
            url(
                r'^autocomplete/$',
                self.admin_site.admin_view(views.RegistryAutocompleteView.as_view()),
                name='{app_label}_{model_name}_autocomplete'.format(**info)
            ),
            url(
                r'^autocomplete/customer/$',
                self.admin_site.admin_view(views.RegistryCustomerAutocompleteView.as_view()),
                name='{app_label}_{model_name}_autocomplete_customer'.format(**info)
            ),
            url(
                r'^autocomplete/supplier/$',
                self.admin_site.admin_view(views.RegistrySupplierAutocompleteView.as_view()),
                name='{app_label}_{model_name}_autocomplete_supplier'.format(**info)
            ),
        ]
        return urls + super().get_urls()


@admin.register(models.Child)
class ChildAdmin(VersionAdmin):
    list_display = ('description', 'parent_1', 'parent_2')
    list_display_links = ('description',)
    search_fields = ('description',)
    form = forms.ChildForm
    fieldsets = [
        (None, {
            'fields': [
                ('last_name', 'first_name',),
                ('parent_1', 'parent_2',),
            ]
        }),
    ]

    def get_urls(self):
        info = dict(app_label=self.model._meta.app_label, model_name=self.model._meta.model_name)
        urls = [
            url(
                r'^autocomplete/$',
                self.admin_site.admin_view(views.ChildAutocompleteView.as_view()),
                name='{app_label}_{model_name}_autocomplete'.format(**info)
            ),
        ]
        return urls + super().get_urls()
