from mock import patch, Mock
from django.test import TestCase
from django.core.management import execute_from_command_line
from favicon.management.commands.generate_favicon import Command as Generate
from favicon.management.commands.delete_favicon import Command as Delete
from favicon.tests.utils import HANDLED_FILES, BASE_IMG, EXPECTED_FILES
from favicon.utils import generate
from favicon.tests.utils import FakeStorage


@patch('favicon.management.commands.generate_favicon.input',
       return_value='Yes')
class GenerateFaviconCommandTest(TestCase):
    def setUp(self):
        self.command = Generate()

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_execute_from_command_line(self, *mocks):
        execute_from_command_line(['', 'generate_favicon', BASE_IMG])
        self.assertTrue(HANDLED_FILES['written_files'])
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertTrue(content.size)

    @patch('favicon.tests.utils.FakeStorage.post_process')
    def test_post_process(self, *mocks):
        execute_from_command_line(['', 'generate_favicon', BASE_IMG,
                                   '--post-process'])
        self.assertTrue(HANDLED_FILES['written_files'])
        self.assertTrue(mocks[0].called)

    def test_no_input(self, *mocks):
        execute_from_command_line(['', 'generate_favicon', BASE_IMG,
                                   '--noinput'])
        self.assertTrue(HANDLED_FILES['written_files'])
        self.assertFalse(mocks[0].called)

    @patch('favicon.management.commands.generate_favicon.input',
           return_value='No')
    def test_dry_run(self, *mocks):
        execute_from_command_line(['', 'generate_favicon', BASE_IMG,
                                   '--dry-run'])
        self.assertFalse(HANDLED_FILES['written_files'])

    @patch('favicon.tests.utils.FakeStorage.post_process')
    def test_dry_run_post_process(self, *mocks):
        execute_from_command_line(['', 'generate_favicon', BASE_IMG,
                                   '--post-process', '--dry-run'])
        self.assertFalse(HANDLED_FILES['written_files'])
        self.assertFalse(mocks[0].called)

    def test_prefix(self, *mocks):
        prefix = 'foo/'
        expected_files = [prefix+fi for fi in EXPECTED_FILES]
        execute_from_command_line(['', 'generate_favicon', BASE_IMG,
                                   '--prefix=foo/'])
        self.assertTrue(HANDLED_FILES['written_files'])
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, expected_files)
            self.assertTrue(content.size)

    def test_source_file_from_storage(self, *mocks):
        HANDLED_FILES['written_files']['logo.png'] = open(BASE_IMG, 'rb')
        execute_from_command_line(['', 'generate_favicon', 'file://logo.png'])
        self.assertTrue(HANDLED_FILES['written_files'])
        for name, content in HANDLED_FILES['written_files'].items():
            if 'logo.png' == name:
                continue
            self.assertIn(name, EXPECTED_FILES)
            self.assertTrue(content.size)

    @patch('favicon.management.commands.generate_favicon.urlopen',
           return_value=Mock(fp=open(BASE_IMG, 'rb')))
    def test_source_file_from_http(self, *mocks):
        execute_from_command_line(['', 'generate_favicon',
                                   'http://example.com/logo.png'])
        self.assertTrue(HANDLED_FILES['written_files'])
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertTrue(content.size)
        self.assertTrue(mocks[0].called)


@patch('favicon.management.commands.delete_favicon.input',
       return_value='Yes')
class DeleteFaviconCommandTest(TestCase):
    def setUp(self):
        self.command = Delete()
        self.storage = FakeStorage()
        generate(BASE_IMG, self.storage)

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_execute_from_command_line(self, *mocks):
        execute_from_command_line(['', 'delete_favicon'])
        self.assertTrue(HANDLED_FILES['deleted_files'])

    def test_dry_run(self, *mocks):
        execute_from_command_line(['', 'delete_favicon', '--dry-run'])
        self.assertFalse(HANDLED_FILES['deleted_files'])

    def test_no_input(self, *mocks):
        execute_from_command_line(['', 'delete_favicon', '--noinput'])
        self.assertTrue(HANDLED_FILES['deleted_files'])
        self.assertFalse(mocks[0].called)

    def test_prefix(self, *mocks):
        prefix = 'foo/'
        expected_files = [prefix+fi for fi in EXPECTED_FILES]

        generate(BASE_IMG, self.storage, prefix)
        execute_from_command_line(['', 'delete_favicon', '--prefix=foo/'])

        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertNotIn(name, expected_files)
        for name, content in HANDLED_FILES['deleted_files'].items():
            self.assertIn(name, expected_files)
            self.assertNotIn(name, EXPECTED_FILES)
