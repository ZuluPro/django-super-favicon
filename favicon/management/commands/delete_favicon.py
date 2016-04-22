"""Delete favicons from storage."""
from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import get_storage_class
from django.utils import six
from favicon import settings
from favicon.utils import delete

input = raw_input if six.PY2 else input


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--prefix', '-p', default=None,
                            help="Prefix included in files' names")
        parser.add_argument('--noinput', action='store_true', default=False,
                            help="Do NOT prompt the user for input of any kind.")
        parser.add_argument('--dry-run', '-n', action='store_true', default=False,
                            help="Do everything except modify the filesystem.")

    def handle(self, *args, **options):
        prefix = options['prefix']
        storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)

        if not options['noinput']:
            answer = input("Are you sure you want to continue? [Y/n]")
            if answer.lower().startswith('n'):
                self.stdout.write('Quitting')
                return

        self.stdout.write('Launch favicon deleting')
        if options['dry_run']:
            self.stdout.write('No operation launched')
        else:
            delete(storage, prefix)
