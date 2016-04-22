from django.test import TestCase
from django.core.management import execute_from_command_line
from favicon.management.commands.generate_favicon import Command as Generate
from favicon.management.commands.delete_favicon import Command as Delete
from favicon.tests.utils import HANDLED_FILES, BASE_IMG, EXPECTED_FILES
from favicon.utils import generate
from favicon.tests.utils import FakeStorage


class GenerateFaviconCommandTest(TestCase):
    def setUp(self):
        self.command = Generate()

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


class DeleteFaviconCommandTest(TestCase):
    def setUp(self):
        self.command = Delete()
        self.storage = FakeStorage()
        generate(BASE_IMG, self.storage)

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_execute_from_command_line(self):
        execute_from_command_line(['', 'delete_favicon'])
        for name, content in HANDLED_FILES['deleted_files'].items():
            self.assertIn(name, EXPECTED_FILES)

    def test_handle(self):
        self.command.handle()
        for name, content in HANDLED_FILES['deleted_files'].items():
            self.assertIn(name, EXPECTED_FILES)
