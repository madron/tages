import json
from django.test import override_settings
from graphene_django.utils.testing import GraphQLTestCase
from . import factories


class RegistryTest(GraphQLTestCase):
    def test_description(self):
        factories.RegistryFactory(registry_type='private', last_name='Black', first_name='Joe')
        response = self.query(
            '''
            query{
                registries {
                    description
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'registries': [{'description': 'Joe Black'}]})

    def test_filter_id(self):
        factories.RegistryFactory(id=1, registry_type='private', last_name='Black', first_name='Joe')
        factories.RegistryFactory(id=2, registry_type='private', last_name='Brown', first_name='John')
        response = self.query(
            '''
            query{
                registries (id: 2) {
                    description
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'registries': [{'description': 'John Brown'}]})

    def test_filter_description(self):
        factories.RegistryFactory(id=1, registry_type='private', last_name='Black', first_name='Joe')
        factories.RegistryFactory(id=2, registry_type='private', last_name='Brown', first_name='John')
        response = self.query(
            '''
            query{
                registries (description_Icontains: "bl") {
                    description
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'registries': [{'description': 'Joe Black'}]})
