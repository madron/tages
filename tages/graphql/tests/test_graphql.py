import json
from django.test import override_settings
from graphene_django.utils.testing import GraphQLTestCase


@override_settings(VERSION='1.0.1')
class VersionTest(GraphQLTestCase):
    def test_ok(self):
        response = self.query(
            '''
            query{version}
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, dict(version='1.0.1'))
