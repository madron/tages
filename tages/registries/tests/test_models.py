from datetime import date
from django.urls import reverse
from django.test import TestCase
from . import factories
from .. import models


class RegistryModelTest(TestCase):
    def test_manager_actives(self):
        factories.RegistryFactory(deactivation_date=date(2017, 1, 1))
        self.assertEqual(models.Registry.actives.all().count(), 0)

    def test_str_deactivated(self):
        registry = factories.RegistryFactory(
            type='company', business_name='Acme', deactivation_date=date(2017, 1, 1))
        self.assertEqual(str(registry), 'Acme (Deactivated)')

    def test_description_private(self):
        registry = factories.RegistryFactory(type='private', last_name='Holovaty', first_name='Adrian')
        self.assertEqual(registry.description, 'Adrian Holovaty')

    def test_description_company(self):
        registry = factories.RegistryFactory(type='company', business_name='Acme')
        self.assertEqual(registry.description, 'Acme')

    def test_description_individual_company(self):
        registry = factories.RegistryFactory(type='individual_company', business_name='Acme')
        self.assertEqual(registry.description, 'Acme')

    def test_description_public_administration(self):
        registry = factories.RegistryFactory(type='public_administration', business_name='Acme')
        self.assertEqual(registry.description, 'Acme')

    def test_get_url(self):
        registry = factories.RegistryFactory(id=1)
        self.assertEqual(
            registry.get_url(),
            reverse('admin:registries_registry_change', args=(registry.pk,)),
        )

    def test_get_link(self):
        registry = factories.RegistryFactory(id=1, type='company', business_name='Acme')
        self.assertEqual(
            registry.get_link(),
            '<a href="/admin/registries/registry/1/change/">Acme</a>',
        )

    def test_insert_date(self):
        registry = factories.RegistryFactory()
        self.assertEqual(registry.insert_date, date.today())

    def test_get_country(self):
        registry = factories.RegistryFactory(country='GB')
        self.assertEqual(registry.get_country(), 'GB')

    def test_get_postal_address(self):
        registry = factories.RegistryFactory(
            type='private',
            last_name='Black',
            first_name='Joe',
            country='GB',
            province='LDN',
            city='London',
            address='High Street Kinsington',
            street_number='1',
            zip_code='W8',
        )
        self.assertEqual(registry.get_postal_address(), 'Joe Black\nHigh Street Kinsington 1\nW8 London LDN')

    def test_get_postal_address_no_street_number(self):
        registry = factories.RegistryFactory(
            type='private',
            last_name='Black',
            first_name='Joe',
            country='GB',
            province='LDN',
            city='London',
            address='High Street Kinsington',
            street_number='',
            zip_code='W8',
        )
        self.assertEqual(registry.get_postal_address(), 'Joe Black\nHigh Street Kinsington\nW8 London LDN')

    def test_get_postal_address_no_province(self):
        registry = factories.RegistryFactory(
            type='private',
            last_name='Black',
            first_name='Joe',
            country='GB',
            city='London',
            address='High Street Kinsington',
            street_number='1',
            zip_code='W8',
        )
        self.assertEqual(registry.get_postal_address(), 'Joe Black\nHigh Street Kinsington 1\nW8 London')

    def test_full_address(self):
        registry = factories.RegistryFactory(
            type='private',
            last_name='Black',
            first_name='Joe',
            country='GB',
            city='London',
            address='High Street Kinsington',
            street_number='1',
            zip_code='W8',
        )
        self.assertEqual(registry.full_address, 'High Street Kinsington 1, London')


class ChildModelTest(TestCase):
    def test_str(self):
        obj = factories.ChildFactory(first_name='Bobby', last_name='Little')
        self.assertEqual(str(obj), 'Bobby Little')
