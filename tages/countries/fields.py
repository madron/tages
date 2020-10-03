import django_countries.fields
from . import widgets


class CountryFormField(django_countries.fields.LazyTypedChoiceField):
    widget = widgets.CountrySelect


class CountryField(django_countries.fields.CountryField):
    def formfield(self, **kwargs):
        argname = 'choices_form_class'
        if argname not in kwargs:
            kwargs[argname] = CountryFormField
        field = super(CountryField, self).formfield(**kwargs)
        return field
