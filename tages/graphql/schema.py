import graphene
from django.conf import settings
from tages.registries import schema as registries_schema


class Query(
       registries_schema.Query,
       graphene.ObjectType,
    ):
    version = graphene.String(default_value=settings.VERSION)


schema = graphene.Schema(query=Query)
