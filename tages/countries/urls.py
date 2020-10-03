from django.conf.urls import url
from . import views

app_name = 'countries'
urlpatterns = [
    url(
        r'^autocomplete/$',
        views.CountryAutocompleteView.as_view(),
        name='autocomplete'
    ),
]
