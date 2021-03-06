from django.test import TestCase
from . import factories
from ..forms import RegistryForm, ChildForm


class RegistryFormTest(TestCase):
    def test_clean_ko(self):
        data = dict()
        form = RegistryForm(data)
        self.assertEqual(form.errors['registry_type'], ['This field is required.'])
        self.assertEqual(len(form.errors), 1)

    def test_clean_business_name_company(self):
        data = dict(registry_type='company')
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])

    def test_clean_business_name_individual_company(self):
        data = dict(registry_type='individual_company')
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])

    def test_clean_business_name_public_administration(self):
        data = dict(registry_type='public_administration')
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])

    def test_clean_business_name_organization(self):
        data = dict(registry_type='organization')
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])

    def test_clean_last_name_private(self):
        data = dict(registry_type='private')
        form = RegistryForm(data)
        self.assertEqual(form.errors['last_name'], ['This field is required.'])


class RegistryFormOtherCountryTest(TestCase):
    def test_clean_ok(self):
        data = dict(
            country='GB',
            registry_type='company',
            business_name='Acme',
            vat_number='not_going_to_validate',
        )
        form = RegistryForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_ko(self):
        data = dict(
            country='GB',
            registry_type='company',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])
        self.assertEqual(len(form.errors), 1)


class RegistryFormItCompanyTest(TestCase):
    def test_clean_ok(self):
        data = dict(
            country='IT',
            registry_type='company',
            business_name='Acme',
            vat_number='00146089990',
            social_security_number='00146089990',
        )
        form = RegistryForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_ko(self):
        data = dict(
            country='IT',
            registry_type='company',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])
        self.assertEqual(form.errors['vat_number'], ['This field is required.'])
        self.assertEqual(form.errors['social_security_number'], ['This field is required.'])
        self.assertEqual(len(form.errors), 3)

    def test_clean_ssn_ko(self):
        data = dict(
            country='IT',
            registry_type='company',
            social_security_number='RSSMRA85T10A562S',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['social_security_number'], ['Enter a valid VAT number.'])

    def test_clean_ssn_supplier(self):
        data = dict(
            country='IT',
            registry_type='company',
            customer=False,
            supplier=True,
            social_security_number='',
        )
        form = RegistryForm(data)
        self.assertNotIn('social_security_number', form.errors)

    def test_clean_vat_number_ko(self):
        data = dict(
            country='IT',
            registry_type='company',
            vat_number='00146089991',
            social_security_number='00146089991',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['Enter a valid VAT number.'])
        self.assertEqual(form.errors['social_security_number'], ['Enter a valid VAT number.'])

    def test_clean_vat_number_ko_organization_8(self):
        data = dict(
            country='IT',
            registry_type='company',
            vat_number='86334519757',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['VAT number lined up for organizations.'])

    def test_clean_vat_number_ko_organization_9(self):
        data = dict(
            country='IT',
            registry_type='company',
            vat_number='96334519756',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['VAT number lined up for organizations.'])


class RegistryFormItPublicAdministrationTest(TestCase):
    def test_clean_ok(self):
        data = dict(
            country='IT',
            registry_type='public_administration',
            business_name='Acme',
            social_security_number='00146089990',
        )
        form = RegistryForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_ko(self):
        data = dict(
            country='IT',
            registry_type='public_administration',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])
        self.assertEqual(form.errors['social_security_number'], ['This field is required.'])
        self.assertEqual(len(form.errors), 2)

    def test_clean_ssn_ko(self):
        data = dict(
            country='IT',
            registry_type='public_administration',
            social_security_number='RSSMRA85T10A562S',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['social_security_number'], ['Enter a valid VAT number.'])

    def test_clean_vat_number_ko_organization_8(self):
        data = dict(
            country='IT',
            registry_type='public_administration',
            vat_number='86334519757',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['VAT number lined up for organizations.'])

    def test_clean_vat_number_ko_organization_9(self):
        data = dict(
            country='IT',
            registry_type='public_administration',
            vat_number='96334519756',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['VAT number lined up for organizations.'])



class RegistryFormItOrganizationTest(TestCase):
    def test_clean_ok(self):
        data = dict(
            country='IT',
            registry_type='organization',
            business_name='Acme',
            social_security_number='86334519757',
        )
        form = RegistryForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_ko(self):
        data = dict(
            country='IT',
            registry_type='organization',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])
        self.assertEqual(form.errors['social_security_number'], ['This field is required.'])
        self.assertEqual(len(form.errors), 2)

    def test_clean_ssn_ko(self):
        data = dict(
            country='IT',
            registry_type='organization',
            social_security_number='RSSMRA85T10A562S',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['social_security_number'], ['Enter a valid VAT number.'])


class RegistryFormItIndividualCompanyTest(TestCase):
    def test_clean_ok(self):
        data = dict(
            country='IT',
            registry_type='individual_company',
            business_name='Black',
            last_name='Black',
            first_name='Joe',
            vat_number='00146089990',
            social_security_number='RSSMRA85T10A562S',
        )
        form = RegistryForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_ko(self):
        data = dict(
            country='IT',
            registry_type='individual_company',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['business_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['vat_number'], ['This field is required.'])
        self.assertEqual(form.errors['social_security_number'], ['This field is required.'])
        self.assertEqual(len(form.errors), 5)

    def test_clean_vat_number_ko_organization_8(self):
        data = dict(
            country='IT',
            registry_type='individual_company',
            vat_number='86334519757',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['VAT number lined up for organizations.'])

    def test_clean_vat_number_ko_organization_9(self):
        data = dict(
            country='IT',
            registry_type='individual_company',
            vat_number='96334519756',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['vat_number'], ['VAT number lined up for organizations.'])



class RegistryFormItPrivateTest(TestCase):
    def test_clean_ok(self):
        data = dict(
            country='IT',
            registry_type='private',
            last_name='Black',
            first_name='Joe',
            social_security_number='RSSMRA85T10A562S',
        )
        form = RegistryForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_ko(self):
        data = dict(
            registry_type='private',
        )
        form = RegistryForm(data)
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(len(form.errors), 2)


class ChildFormTest(TestCase):
    def test_clean_ko(self):
        data = dict()
        form = ChildForm(data)
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['parent_1'], ['This field is required.'])
        self.assertEqual(len(form.errors), 3)

    def test_clean_ok(self):
        parent = factories.RegistryFactory()
        data = dict(first_name='Bobby', last_name='Little', parent_1=parent.pk)
        form = ChildForm(data)
        self.assertTrue(form.is_valid())
