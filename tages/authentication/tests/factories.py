import factory
from django.contrib.auth import models


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'group{}'.format(n))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ('username',)

    username = 'test'
    is_active = True
    is_superuser = True
    is_staff = True
    # 'pass'
    password = 'pbkdf2_sha256$12000$LWhlUQyAntYP$FtxgZ9CnZBTbrvcjHJO6StuAJoQqMRDRTFXzYtxRRhg='
    email = 'test@example.com'

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted:
            for group in extracted:
                self.groups.add(group)
