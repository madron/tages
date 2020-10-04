import graphene
from graphene.relay import Node
from graphene_django import DjangoObjectType
from tages.graphql.utils import DjangoFilterOptimizedConnectionField
from . import models


class RegistryNode(DjangoObjectType):
    class Meta:
        model = models.Registry
        exclude = ['registry_type', 'customer', 'supplier']
        interfaces = [Node]
        filter_fields = dict(
            last_name=['exact', 'icontains'],
            first_name=['exact', 'icontains'],
            description=['exact', 'icontains'],
        )


class ChildNode(DjangoObjectType):
    class Meta:
        model = models.Child
        fileds = '__all__'
        interfaces = [Node]
        filter_fields = dict(
            last_name=['exact', 'icontains'],
            first_name=['exact', 'icontains'],
            description=['exact', 'icontains'],
        )


class Query(graphene.ObjectType):
    # registry = Node.Field(RegistryNode)
    registries = DjangoFilterOptimizedConnectionField(RegistryNode)
    # child = Node.Field(ChildNode)
    children = DjangoFilterOptimizedConnectionField(ChildNode)
