import graphene
from django.conf import settings


class Query(graphene.ObjectType):
    version = graphene.String(default_value=settings.VERSION)


schema = graphene.Schema(query=Query)
