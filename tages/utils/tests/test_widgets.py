from django.test import TestCase
from .. import widgets


class AutocompleteSelectTest(TestCase):
    def test_get_label_for_value_ko(self):
        class AutocompleteSelect(widgets.AutocompleteSelect):
            model = None

        with self.assertRaises(NotImplementedError) as cm:
            AutocompleteSelect().get_label_for_value('12')
        exception = cm.exception
        self.assertEqual(
            exception.args,
            ('subclasses of AutocompleteSelect must override get_label_for_value() method if a model is not provided.',)
        )
