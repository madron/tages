from django import forms
from django.utils.translation import ugettext as _
from localflavor.it.forms import ITVatNumberField, ITSocialSecurityNumberField
from tages.utils.exceptions import FieldRequiredError
from . import models
from . import widgets


class RegistryForm(forms.ModelForm):
    field_order = [
        'registry_type',
        'country',
        'business_name',
        'last_name',
        'first_name',
        'customer',
        'supplier',
        'vat_number',
        'social_security_number',
        'external_id',
        'deactivation_date',
    ]

    class Meta:
        model = models.Registry
        fields = ('__all__')
        widgets = dict(
            vat_number=forms.TextInput(attrs={'size': '15'}),
            social_security_number=forms.TextInput(attrs={'size': '15'}),
            external_id=forms.TextInput(attrs={'size': '10'}),
            # Address
            province=forms.TextInput(attrs={'size': '5'}),
            city=forms.TextInput(attrs={'size': '20'}),
            address=forms.TextInput(attrs={'size': '20'}),
            zip_code=forms.TextInput(attrs={'size': '5'}),
            street_number=forms.TextInput(attrs={'size': '5'}),
            # Contacts
            phone_number=forms.TextInput(attrs={'size': '12'}),
            fax_number=forms.TextInput(attrs={'size': '12'}),
            email=forms.TextInput(attrs={'size': '30'}),
            pec=forms.TextInput(attrs={'size': '30'}),
            url=forms.TextInput(attrs={'size': '20'}),

        )

    class Media:
        css = dict(
            all=('registries/css/registry_change_form.css',),
        )

    def clean_business_name(self):
        value = self.cleaned_data['business_name']
        registry_type = self.cleaned_data.get('registry_type', None)
        if registry_type in ['company', 'individual_company', 'public_administration', 'organization']:
            if not value:
                raise FieldRequiredError()
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']
        registry_type = self.cleaned_data.get('registry_type', None)
        if registry_type in ('private', 'individual_company'):
            if not value:
                raise FieldRequiredError()
        return value

    def clean_first_name(self):
        value = self.cleaned_data['first_name']
        registry_type = self.cleaned_data.get('registry_type', None)
        if registry_type in ('private', 'individual_company'):
            if not value:
                raise FieldRequiredError()
        return value

    def clean_vat_number(self):
        value = self.cleaned_data['vat_number']
        country = self.cleaned_data.get('country', None)
        # Italy
        if country == 'IT':
            registry_type = self.cleaned_data.get('registry_type', None)
            required = False
            if registry_type in ['company', 'individual_company']:
                required = True
            value = ITVatNumberField(required=required).clean(value)
            if value.startswith('8') or value.startswith('9'):
                if not registry_type == 'organization':
                    raise forms.ValidationError(_('VAT number lined up for organizations.'))
        return value

    def clean_social_security_number(self):
        value = self.cleaned_data['social_security_number']
        registry_type = self.cleaned_data.get('registry_type', None)
        country = self.cleaned_data.get('country', None)
        # Italy
        if country == 'IT':
            required = True
            if self.cleaned_data['supplier'] and not self.cleaned_data['customer']:
                required = False
            field = dict(
                private=ITSocialSecurityNumberField(required=required),
                company=ITVatNumberField(required=required),
                individual_company=ITSocialSecurityNumberField(required=required),
                public_administration=ITVatNumberField(required=required),
                organization=ITVatNumberField(required=required),
            )
            return field[registry_type].clean(value)
        return value


class ChildForm(forms.ModelForm):
    field_order = [
        'first_name',
        'last_name',
        'parent_1',
        'parent_2',
    ]

    class Meta:
        model = models.Child
        fields = ('__all__')
        widgets = dict(
            first_name=forms.TextInput(attrs={'size': '15'}),
            last_name=forms.TextInput(attrs={'size': '15'}),
        )
