import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import get_storage_class
from favicon import settings
from favicon.utils import generate


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs=1, type=str,
                            help="Input file used to generate favicons")

    def handle(self, *args, **options):
        source_file = options['source_file'][0]
        if not os.path.exists(source_file):
            raise CommandError("File '%s' does not exist." % source_file)
        storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)
        generate(source_file, storage)
