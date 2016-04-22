import re
from django.test import TestCase
from PIL import Image
from favicon.tests.utils import HANDLED_FILES, BASE_IMG, EXPECTED_FILES,\
    FakeStorage
from favicon.utils import generate, delete, PNG_SIZES, WINDOWS_PNG_SIZES

SRC_REG = re.compile(r'src="/static/([^"]*)"')


class GenerateTest(TestCase):
    def setUp(self):
        self.storage = FakeStorage()

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_generate(self):
        generate(BASE_IMG, self.storage)
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertTrue(content.size)
        # Test ICO file
        ico = self.storage._open('favicon.ico')
        self.assertEqual(Image.open(ico).format, 'ICO')
        # Test PNG
        for size in PNG_SIZES:
            name = 'favicon-%d.png' % size
            self.assertTrue(self.storage.exists(name))
            png = self.storage._open(name)
            img = Image.open(png)
            self.assertEqual(img.format, 'PNG')
            self.assertEqual(img.size, (size, size))
        # Test Windows PNG
        for size, name in WINDOWS_PNG_SIZES:
            self.assertTrue(self.storage.exists(name))
            png = self.storage._open(name)
            img = Image.open(png)
            self.assertEqual(img.format, 'PNG')
            if size[0] != size[1] or size[0] > 440:
                continue
            self.assertEqual(img.size, size)
        # Test ieconfig.xml
        ieconfig = self.storage._open('ieconfig.xml').read()
        for name in SRC_REG.findall(ieconfig):
            self.assertTrue(self.storage.exists(name))

    def test_generate_with_prefix(self):
        prefix = 'foo/'
        expected_files = [prefix+fi for fi in EXPECTED_FILES]

        generate(BASE_IMG, self.storage, prefix)
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, expected_files)
            self.assertTrue(content.size)


class DeleteTest(TestCase):
    def setUp(self):
        self.storage = FakeStorage()
        generate(BASE_IMG, self.storage)

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_delete(self):
        delete(self.storage)
        self.assertFalse(HANDLED_FILES['written_files'])
        self.assertTrue(HANDLED_FILES['deleted_files'])

    def test_delete_not_existing(self):
        delete(self.storage)
        delete(self.storage)
        self.assertFalse(HANDLED_FILES['written_files'])
        self.assertTrue(HANDLED_FILES['deleted_files'])

    def test_delete_with_prefix(self):
        prefix = 'foo/'
        expected_files = [prefix+fi for fi in EXPECTED_FILES]

        generate(BASE_IMG, self.storage, prefix)
        delete(self.storage, prefix)
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertNotIn(name, expected_files)
        for name, content in HANDLED_FILES['deleted_files'].items():
            self.assertIn(name, expected_files)
            self.assertNotIn(name, EXPECTED_FILES)
