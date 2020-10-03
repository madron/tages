import json
from django.urls import reverse
from django.test import TestCase


class CountryAutocompleteViewTest(TestCase):
    def setUp(self):
        self.url = reverse('countries:autocomplete')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(len(data.keys()), 2)
        # pagination
        pagination = data['pagination']
        self.assertEqual(pagination, dict(more=False))
        # results
        results = data['results']
        self.assertTrue(len(results) > 200)
        self.assertEqual(results[0], dict(id='AF', text='Afghanistan'))

    def test_filter(self):
        response = self.client.get(self.url, dict(term='nited'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        # results
        results = data['results']
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0], {'id': 'AE', 'text': 'United Arab Emirates'})
        self.assertEqual(results[1], {'id': 'GB', 'text': 'United Kingdom'})
        self.assertEqual(results[2], {'id': 'UM', 'text': 'United States Minor Outlying Islands'})
        self.assertEqual(results[3], {'id': 'US', 'text': 'United States of America'})

    def test_filter_lowercase(self):
        response = self.client.get(self.url, dict(term='king'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        # results
        results = data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], {'id': 'GB', 'text': 'United Kingdom'})
