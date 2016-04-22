from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import get_storage_class
from favicon import settings
from favicon.utils import delete


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)
        delete(storage)
