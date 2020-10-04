import graphene
import graphene_django_optimizer as gql_optimizer
from django_filters.filterset import FilterSet
from graphene_django import DjangoObjectType
from graphene_django.filter.utils import get_filtering_args_from_filterset
from . import models


class RegistryFilter(FilterSet):
    class Meta:
        model = models.Registry
        fields = dict(
            id=['exact'],
            last_name=['exact', 'icontains'],
            first_name=['exact', 'icontains'],
            description=['exact', 'icontains'],
        )


class RegistryType(DjangoObjectType):
    class Meta:
        model = models.Registry
        exclude = ['registry_type', 'customer', 'supplier']


class ChildFilter(FilterSet):
    class Meta:
        model = models.Child
        fields = dict(
            id=['exact'],
            last_name=['exact', 'icontains'],
            first_name=['exact', 'icontains'],
            description=['exact', 'icontains'],
        )


class ChildType(DjangoObjectType):
    class Meta:
        model = models.Child
        fileds = '__all__'


class Query(graphene.ObjectType):
    registries = graphene.List(RegistryType, **get_filtering_args_from_filterset(RegistryFilter, None))
    children = graphene.List(ChildType, **get_filtering_args_from_filterset(ChildFilter, None))

    def resolve_registries(root, info, **kwargs):
        return gql_optimizer.query(models.Registry.objects.filter(**kwargs), info)

    def resolve_children(root, info, **kwargs):
        return gql_optimizer.query(models.Child.objects.filter(**kwargs), info)
