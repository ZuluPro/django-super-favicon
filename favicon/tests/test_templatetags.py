import re
from django.test import TestCase
from favicon.templatetags.favicon import get_favicons, favicon_url
from favicon.tests.utils import HANDLED_FILES, BASE_IMG, FakeStorage, BASE_URL
from favicon.utils import generate

SRC_REG = re.compile(r'(?:href|content|src)="%s([^"]*)"' % BASE_URL)


class GetFaviconsTest(TestCase):
    def setUp(self):
        self.storage = FakeStorage()

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_get_favicons(self):
        generate(BASE_IMG, self.storage)
        html = get_favicons()
        urls = SRC_REG.findall(html)
        self.assertTrue(urls)
        for name in urls:
            self.assertTrue(self.storage.exists(name))

    def test_get_favicons_with_prefix(self):
        prefix = 'foo/'
        generate(BASE_IMG, self.storage, prefix)
        html = get_favicons(prefix)
        urls = SRC_REG.findall(html)
        self.assertTrue(urls)
        for name in urls:
            self.assertTrue(self.storage.exists(name))


class FaviconUrlTest(TestCase):
    def test_favicon_url(self):
        url = favicon_url('foo.png')
        self.assertEqual(FakeStorage().url('foo.png'), url)

    def test_favicon_url_with_prefix(self):
        url = favicon_url('foo.png', 'bar/')
        self.assertEqual(FakeStorage().url('bar/foo.png'), url)
