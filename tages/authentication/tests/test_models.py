from django.test import TestCase
from . import factories


class GroupModelTest(TestCase):
    def test_str(self):
        group = factories.GroupFactory(name='group1')
        self.assertEqual(str(group), 'group1')

    def test_build(self):
        group = factories.GroupFactory.build(name='group1')
        self.assertEqual(str(group), 'group1')

    def test_create(self):
        group = factories.GroupFactory.create(name='group1')
        self.assertEqual(str(group), 'group1')


class UserModelTest(TestCase):
    def test_str(self):
        user = factories.UserFactory(username='user1')
        self.assertEqual(str(user), 'user1')

    def test_emtpy_groups(self):
        user = factories.UserFactory(username='user1', groups=[])
        self.assertEqual(user.groups.count(), 0)

    def test_group(self):
        group = factories.GroupFactory(name='group1')
        user = factories.UserFactory(username='user1', groups=[group])
        self.assertEqual(user.groups.count(), 1)
        self.assertEqual(user.groups.all()[0], group)
