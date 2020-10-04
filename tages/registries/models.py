from datetime import date
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from tages.countries.defaults import COUNTRIES_DEFAULT
from tages.countries.fields import CountryField
from tages.utils.web import email_link, url_link


REGISTRY_TYPES = (
    ('private', _('Private')),
    ('company', _('Company')),
    ('individual_company', _('Individual company')),
    ('public_administration', _('Public administration')),
    ('organization', _('Organization')),
)


class RegistryActiveManager(models.Manager):
    def get_queryset(self):
        qs = super(RegistryActiveManager, self).get_queryset()
        return qs.filter(deactivation_date__isnull=True)


class Registry(models.Model):
    registry_type = models.CharField(_('registry type'), max_length=50, choices=REGISTRY_TYPES, default='private', db_index=True)
    country = CountryField(_('country'), default=COUNTRIES_DEFAULT, db_index=True)
    business_name = models.CharField(_('business name'), max_length=200, blank=True, null=True, db_index=True)
    last_name = models.CharField(_('last name'), max_length=200, blank=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=200, blank=True, db_index=True)
    description = models.CharField(_('description'), max_length=200, db_index=True, editable=False, default='')
    customer = models.BooleanField(_('customer'), default=True, db_index=True)
    supplier = models.BooleanField(_('supplier'), default=False, db_index=True)
    vat_number = models.CharField(_('vat number'), max_length=50, blank=True, db_index=True)
    social_security_number = models.CharField(_('social security number'), max_length=50, blank=True, db_index=True)
    external_id = models.CharField(_('external id'), max_length=50, blank=True, db_index=True)
    # Address
    country = CountryField(_('country'), default=COUNTRIES_DEFAULT, blank=True, db_index=True)
    province = models.CharField(_('province'), max_length=200, blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    address = models.CharField(_('address'), max_length=200, blank=True)
    street_number = models.CharField(_('street number'), max_length=50, blank=True)
    zip_code = models.CharField(_('zip code'), max_length=50, blank=True)
    # Contacts
    phone_number = models.CharField(_('phone number'), max_length=200, blank=True)
    fax_number = models.CharField(_('fax number'), max_length=200, blank=True)
    email = models.EmailField(_('email'), blank=True)
    pec = models.EmailField(_('pec'), blank=True)
    url = models.URLField(_('url'), blank=True)
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    # Dates
    deactivation_date = models.DateField(_('deactivation date'), blank=True, null=True,
                                         default=None, db_index=True)
    insert_date = models.DateField(_('insert date'), default=date.today, editable=False, db_index=True)

    objects = models.Manager()
    actives = RegistryActiveManager()

    class Meta:
        verbose_name = _('registry')
        verbose_name_plural = _('registries')
        ordering = ['description']

    def __str__(self):
        if self.deactivation_date:
            return ugettext('%(description)s (Deactivated)') % dict(description=self.description)
        return str(self.description)

    def save(self, *args, **kwargs):
        # Description
        if self.registry_type == 'private':
            self.description = ' '.join((self.first_name, self.last_name)).strip()
        else:
            self.description = self.business_name
        # Save
        super(Registry, self).save(*args, **kwargs)

    def get_id(self):
        return self.pk
    get_id.short_description = _('id')
    get_id.admin_order_field = 'pk'

    def active(self):
        return not bool(self.deactivation_date)
    active.short_description = _('active')
    active.admin_order_field = 'deactivation_date'
    active.boolean = True

    def get_url(self):
        info = dict(app_label=self._meta.app_label, model_name=self._meta.model_name)
        url_name = 'admin:{app_label}_{model_name}_change'.format(**info)
        return reverse(url_name, args=(self.pk,))

    def get_link(self):
        return url_link(self.get_url(), label=self.description)
    get_link.short_description = _('registry')
    get_link.admin_order_field = 'description'

    def get_country(self):
        return self.country.code
    get_country.short_description = _('country')
    get_country.admin_order_field = 'country'

    def get_postal_address(self):
        rows = []
        rows.append(str(self.description))
        if self.street_number:
            rows.append('{} {}'.format(self.address, self.street_number))
        else:
            rows.append(str(self.address))
        parts = []
        if self.zip_code:
            parts.append(self.zip_code)
        parts.append(self.city)
        if self.province:
            parts.append(self.province)
        rows.append(' '.join(parts))
        return '\n'.join(rows)

    @property
    def full_address(self):
        return '{} {}, {}'.format(self.address, self.street_number, self.city)


class Child(models.Model):
    first_name = models.CharField(_('first name'), max_length=200, db_index=True)
    last_name = models.CharField(_('last name'), max_length=200, db_index=True)
    description = models.CharField(_('description'), max_length=200, db_index=True, editable=False, default='')
    parent_1 = models.ForeignKey(Registry, verbose_name=_('parent 1'), on_delete=models.RESTRICT,
                                 related_name='parent_1_childs', db_index=True)
    parent_2 = models.ForeignKey(Registry, verbose_name=_('parent 2'), on_delete=models.RESTRICT,
                                 blank=True, null=True, related_name='parent_2_childs', db_index=True)

    class Meta:
        verbose_name = _('child')
        verbose_name_plural = _('children')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return str(self.description)

    def save(self, *args, **kwargs):
        # Description
        self.description = ' '.join((self.first_name, self.last_name)).strip()
        # Save
        super().save(*args, **kwargs)
