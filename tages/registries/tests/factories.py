import factory
from .. import models


class RegistryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Registry

    registry_type = 'private'
    last_name = factory.Sequence(lambda n: 'Surname {0}'.format(n))
    first_name = factory.Sequence(lambda n: 'Name {0}'.format(n))
    customer = True


class RegistryCustomerFactory(RegistryFactory):
    registry_type = 'private'


class ChildFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Child

    last_name = factory.Sequence(lambda n: 'Surname {0}'.format(n))
    first_name = factory.Sequence(lambda n: 'Name {0}'.format(n))
    parent_1 = factory.SubFactory(RegistryFactory)
    parent_2 = factory.SubFactory(RegistryFactory)
