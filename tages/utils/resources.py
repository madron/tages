from django.utils.encoding import force_text
from import_export.resources import ModelResource


class TranslatedModelResource(ModelResource):
    def get_export_headers(self):
        field_names = []
        for field in self.get_export_fields():
            for f in self._meta.model._meta.fields:
                if f.name == field.column_name:
                    if isinstance(f.verbose_name, str):
                        field_names.append(field.column_name)
                    else:
                        field_names.append(f.verbose_name)
        return [force_text(name) for name in field_names]
