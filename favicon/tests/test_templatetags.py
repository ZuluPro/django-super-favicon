import re
from django.test import TestCase
from favicon.templatetags.favicon import get_favicons
from favicon.tests.utils import HANDLED_FILES, BASE_IMG, FakeStorage
from favicon.generators import generate

SRC_REG = re.compile(r'(?:href|content|src)="/static/([^"]*)"')


class GetFaviconsTest(TestCase):
    def setUp(self):
        self.storage = FakeStorage()
        generate(BASE_IMG, self.storage)

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_get_favicons(self):
        html = get_favicons()
        for name in SRC_REG.findall(html):
            self.assertTrue(self.storage.exists(name))
