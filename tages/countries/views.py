import json
from django.http import HttpResponse
from django.views.generic import View
from django_countries import countries


class CountryAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        data = dict(
            pagination=dict(more=False),
            results=self.get_results(),
        )
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_results(self):
        term = self.request.GET.get('term', '').lower()
        if term:
            return [
                dict(id=code, text=name)
                for code, name in list(countries)
                if term in name.lower()
            ]
        return [dict(id=code, text=name) for code, name in list(countries)]
