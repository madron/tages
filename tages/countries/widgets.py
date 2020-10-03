from django_countries import countries
from tages.utils.widgets import AutocompleteSelect


class CountrySelect(AutocompleteSelect):
    url_name = 'countries:autocomplete'

    def get_label_for_value(self, value):
        if value:
            return dict(countries)[value]
        return ''
