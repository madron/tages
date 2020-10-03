from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class WaitForDatabaseTest(TestCase):
    def test_command(self):
        out = StringIO()
        err = StringIO()
        call_command('wait_for_database', '--test-mode', stdout=out, stderr=err)
