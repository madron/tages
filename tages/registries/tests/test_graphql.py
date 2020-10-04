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
                    edges {
                        node {
                            description
                        }
                    }
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'registries': {'edges': [{'node': {'description': 'Joe Black'}}]}})

    def test_filter_description(self):
        factories.RegistryFactory(id=1, registry_type='private', last_name='Black', first_name='Joe')
        factories.RegistryFactory(id=2, registry_type='private', last_name='Brown', first_name='John')
        response = self.query(
            '''
            query{
                registries (description_Icontains: "bl") {
                    edges {
                        node {
                            description
                        }
                    }
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'registries': {'edges': [{'node': {'description': 'Joe Black'}}]}})


class ChildTest(GraphQLTestCase):
    def test_description(self):
        factories.ChildFactory(last_name='Little', first_name='Bobby')
        response = self.query(
            '''
            query{
                children {
                    edges {
                        node {
                            description
                        }
                    }
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'children': {'edges': [{'node': {'description': 'Bobby Little'}}]}})

    def test_filter_description(self):
        factories.ChildFactory(id=1, last_name='Little', first_name='Bobby')
        factories.ChildFactory(id=2, last_name='Little', first_name='Steward')
        response = self.query(
            '''
            query{
                children (description_Icontains: "stew") {
                    edges {
                        node {
                            description
                        }
                    }
                }
            }
            ''',
        )
        self.assertResponseNoErrors(response)
        data = response.json()['data']
        self.assertEqual(data, {'children': {'edges': [{'node': {'description': 'Steward Little'}}]}})
