from django.test import TestCase
from .. import web


class WebTest(TestCase):
    def test_url_link(self):
        text = web.url_link('example.com')
        self.assertEqual(text, '<a href="example.com">example.com</a>')

    def test_url_link_empty(self):
        self.assertEqual(web.url_link(''), u'')

    def test_url_link_label(self):
        text = web.url_link('example.com', label='example')
        self.assertEqual(text, '<a href="example.com">example</a>')

    def test_url_link_title(self):
        text = web.url_link('example.com', title='News')
        self.assertEqual(text, '<a href="example.com" title="News">example.com</a>')

    def test_url_link_label_title(self):
        text = web.url_link('example.com', label='example', title='News')
        self.assertEqual(text, '<a href="example.com" title="News">example</a>')

    def test_email_link(self):
        text = web.email_link('info@example.com')
        self.assertEqual(text, '<a href="mailto:info@example.com" '
                         'title="info@example.com">info@example.com</a>')

    def test_email_link_empty(self):
        self.assertEqual(web.email_link(''), '')

    def test_pdf_link(self):
        text = web.pdf_link('download/document.pdf')
        self.assertEqual(text, '<a href="download/document.pdf" '
                         'title="download/document.pdf" class="icon-book">')

    def test_pdf_link_empty(self):
        self.assertEqual(web.pdf_link(''), u'')
