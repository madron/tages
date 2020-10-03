from django.contrib.admin import widgets
from django.urls import reverse


class AutocompleteSelect(widgets.AutocompleteSelect):
    model = None
    url_name = 'admin:{app_label}_{model_name}_autocomplete'

    def __init__(self, *args, **kwargs):
        super().__init__(None, None, **kwargs)

    def get_url(self):
        if self.model:
            meta = self.model._meta
            info = dict(app_label=meta.app_label, model_name=meta.model_name)
            return reverse(self.url_name.format(**info))
        return reverse(self.url_name)

    def optgroups(self, name, value, attr=None):
        if self.model:
            return super().optgroups(name, value, attr=attr)
        options = []
        for v in value:
            options.append(self.create_option(name, v, self.get_label_for_value(v), False, 0))
        return [(None, options, 0)]

    def get_label_for_value(self, value):
        msg = 'subclasses of AutocompleteSelect must override ' \
            'get_label_for_value() method if a model is not provided.'
        raise NotImplementedError(msg)
