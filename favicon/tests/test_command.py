from django.test import TestCase
from django.core.management import execute_from_command_line
from favicon.management.commands.generate_favicon import Command
from favicon.tests.utils import HANDLED_FILES, BASE_IMG, EXPECTED_FILES


class GenerateFaviconCommandTest(TestCase):
    def setUp(self):
        self.command = Command()

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_execute_from_command_line(self):
        execute_from_command_line(['', 'generate_favicon', BASE_IMG])
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertTrue(content.size)

    def test_handle(self):
        self.command.handle(source_file=[BASE_IMG])
        for name, content in HANDLED_FILES['written_files'].items():
            self.assertIn(name, EXPECTED_FILES)
            self.assertTrue(content.size)
