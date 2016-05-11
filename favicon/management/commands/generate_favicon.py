"""Create favicons and upload into storage."""
import re
from shutil import copyfileobj
from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import get_storage_class
from django.utils import six
from favicon import settings
from favicon.utils import generate

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

input = raw_input if six.PY2 else input

SOURCE_FILE_HELP = """Input file used to generate favicons, example:
'/path/to/myfile.png' : Get from local filesystem root
'path/to/myfile.png' : Get from local filesystem relative path
'file://myfile.png' : Get from static file storage
'http://example.com/myfile.png' : Get from HTTP server
"""


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs=1, type=str,
                            help=SOURCE_FILE_HELP)
        parser.add_argument('--prefix', '-p', default=None,
                            help="Prefix included in new files' names")
        parser.add_argument('--noinput', '-i', action='store_true', default=False,
                            help="Do NOT prompt the user for input of any kind.")
        parser.add_argument('--post-process', action='store_true', default=False,
                            help="Do post process collected files.")
        parser.add_argument('--replace', '-r', action='store_true', default=False,
                            help="Delete file if already existing.")
        parser.add_argument('--dry-run', '-n', action='store_true', default=False,
                            help="Do everything except modify the filesystem.")

    def handle(self, *args, **options):
        source_filename = options['source_file'][0]
        prefix = options['prefix']

        storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)

        if source_filename.startswith('file://'):
            source_filename = source_filename.replace('file://', '')
            source_file = storage.open(source_filename)
        elif re.match(r'^https?://.*$', source_filename):
            response = urlopen(source_filename)
            source_file = six.BytesIO()
            copyfileobj(response.fp, source_file)
            source_file.seek(0)
        else:
            source_file = source_filename

        if not options['noinput']:
            answer = input("Are you sure you want to continue? [Y/n]")
            if answer.lower().startswith('n'):
                self.stdout.write('Quitting')
                return

        self.stdout.write('Launch favicon generation and uploading')
        if options['dry_run']:
            self.stdout.write('No operation launched')
        else:
            generate(source_file, storage, prefix, options['replace'])

        if options['post_process']:
            self.stdout.write('Launch post process')
            if options['dry_run']:
                self.stdout.write('No operation launched')
            else:
                storage.post_process()
