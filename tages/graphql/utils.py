import graphene_django_optimizer as gql_optimizer
from graphene_django.filter import DjangoFilterConnectionField


class DjangoFilterOptimizedConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        qs = super().resolve_queryset(connection, iterable, info, args, filtering_args, filterset_class)
        return gql_optimizer.query(qs, info)


