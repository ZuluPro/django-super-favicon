"""Create favicons and upload into storage."""
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import get_storage_class
from django.utils import six
from favicon import settings
from favicon.utils import generate

input = raw_input if six.PY2 else input


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs=1, type=str,
                            help="Input file used to generate favicons")
        parser.add_argument('--prefix', '-p', default=None,
                            help="Prefix included in new files' names")
        parser.add_argument('--noinput', '-i', action='store_true', default=False,
                            help="Do NOT prompt the user for input of any kind.")
        parser.add_argument('--post-process', action='store_true', default=False,
                            help="Do post process collected files.")
        parser.add_argument('--dry-run', '-n', action='store_true', default=False,
                            help="Do everything except modify the filesystem.")

    def handle(self, *args, **options):
        source_file = options['source_file'][0]
        prefix = options['prefix']
        if not os.path.exists(source_file):
            raise CommandError("File '%s' does not exist." % source_file)
        storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)

        if not options['noinput']:
            answer = input("Are you sure you want to continue? [Y/n]")
            if answer.lower().startswith('n'):
                self.stdout.write('Quitting')
                return

        self.stdout.write('Launch favicon generation and uploading')
        if options['dry_run']:
            self.stdout.write('No operation launched')
        else:
            generate(source_file, storage, prefix)

        if options['post_process']:
            self.stdout.write('Launch post process')
            if options['dry_run']:
                self.stdout.write('No operation launched')
            else:
                storage.post_process()
