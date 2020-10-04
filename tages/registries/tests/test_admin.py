from datetime import date
from django.urls import reverse
from django.test import TestCase
from tages.authentication.tests.factories import UserFactory
from . import factories
from .. import models


class RegistryAdminTest(TestCase):
    def setUp(self):
        user = UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.obj = factories.RegistryFactory()
        self.name = 'admin:registries_registry'
        self.list = reverse('{}_changelist'.format(self.name))

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('{}_add'.format(self.name))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        url = reverse('{}_change'.format(self.name), args=(self.obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        url = reverse('{}_delete'.format(self.name), args=(self.obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_active_default(self):
        obj1 = factories.RegistryFactory(deactivation_date=None)
        obj2 = factories.RegistryFactory(deactivation_date=date(2017, 1, 1))
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)
        url = reverse('admin:registries_registry_change', args=(obj1.pk,))
        self.assertContains(response, url)
        url = reverse('admin:registries_registry_change', args=(obj2.pk,))
        self.assertNotContains(response, url)

    def test_filter_active_no(self):
        obj1 = factories.RegistryFactory(deactivation_date=None)
        obj2 = factories.RegistryFactory(deactivation_date=date(2017, 1, 1))
        data = dict(active='no')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)
        url = reverse('admin:registries_registry_change', args=(obj1.pk,))
        self.assertNotContains(response, url)
        url = reverse('admin:registries_registry_change', args=(obj2.pk,))
        self.assertContains(response, url)

    def test_filter_active_all(self):
        obj1 = factories.RegistryFactory(deactivation_date=None)
        obj2 = factories.RegistryFactory(deactivation_date=date(2017, 1, 1))
        data = dict(active='all')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)
        url = reverse('admin:registries_registry_change', args=(obj1.pk,))
        self.assertContains(response, url)
        url = reverse('admin:registries_registry_change', args=(obj2.pk,))
        self.assertContains(response, url)

    def test_autocomplete(self):
        factories.RegistryFactory(customer=False, supplier=False, registry_type='company', business_name='aaa')
        factories.RegistryFactory(customer=False, supplier=False, registry_type='company', business_name='bbb')
        data = dict(term='aa')
        url = reverse('{}_autocomplete'.format(self.name))
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aaa')
        self.assertNotContains(response, 'bbb')

    def test_autocomplete_not_logged_in(self):
        self.client.logout()
        url = reverse('{}_autocomplete'.format(self.name))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_autocomplete_customer(self):
        factories.RegistryFactory(customer=True, supplier=False, registry_type='company', business_name='aaa')
        factories.RegistryFactory(customer=True, supplier=False, registry_type='company', business_name='bbb')
        data = dict(term='aa')
        url = reverse('{}_autocomplete_customer'.format(self.name))
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aaa')
        self.assertNotContains(response, 'bbb')

    def test_autocomplete_customer_not_logged_in(self):
        self.client.logout()
        url = reverse('{}_autocomplete_customer'.format(self.name))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_autocomplete_supplier(self):
        factories.RegistryFactory(customer=False, supplier=True, registry_type='company', business_name='aaa')
        factories.RegistryFactory(customer=False, supplier=True, registry_type='company', business_name='bbb')
        data = dict(term='aa')
        url = reverse('{}_autocomplete_supplier'.format(self.name))
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aaa')
        self.assertNotContains(response, 'bbb')

    def test_autocomplete_supplier_not_logged_in(self):
        self.client.logout()
        url = reverse('{}_autocomplete_supplier'.format(self.name))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_export_csv(self):
        factories.RegistryFactory(pk=9)
        data = dict(action='export_admin_action', file_format=0, _selected_action=[9])
        response = self.client.post(self.list, data)
        self.assertContains(response, 'id,last name,first name,social security number,external id,deactivation date,insert date')

    def test_insert_date(self):
        factories.RegistryFactory(insert_date=date(2017, 5, 20))
        response = self.client.get(self.list)
        self.assertContains(response, 'Insert date')
        self.assertContains(response, 'May 20, 2017')


class ChildAdminTest(TestCase):
    def setUp(self):
        user = UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.obj = factories.ChildFactory()
        self.name = 'admin:registries_child'
        self.list = reverse('{}_changelist'.format(self.name))

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('{}_add'.format(self.name))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        url = reverse('{}_change'.format(self.name), args=(self.obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        url = reverse('{}_delete'.format(self.name), args=(self.obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_autocomplete(self):
        factories.ChildFactory(last_name='aaa', first_name='Bob')
        factories.ChildFactory(last_name='bbb', first_name='Bob')
        data = dict(term='aa')
        url = reverse('{}_autocomplete'.format(self.name))
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aaa')
        self.assertNotContains(response, 'bbb')

    def test_autocomplete_not_logged_in(self):
        self.client.logout()
        url = reverse('{}_autocomplete'.format(self.name))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
