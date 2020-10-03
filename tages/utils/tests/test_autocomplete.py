from django.test import TestCase
from ..autocomplete import AutocompleteJsonView


class AutocompleteJsonViewTest(TestCase):
    def test_ko(self):
        class AutocompleteTest(AutocompleteJsonView):
            pass
        with self.assertRaises(NotImplementedError) as cm:
            AutocompleteTest().get_queryset()
        exception = cm.exception
        self.assertEqual(
            exception.args,
            ('subclasses of AutocompleteJsonView must provide a get_queryset() method',)
        )
