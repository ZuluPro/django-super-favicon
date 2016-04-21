import os
from django.core.management.base import BaseCommand, CommandError
from PIL import Image
from favicon import settings

PNG_SIZE = (32, 57, 76, 96, 120, 128, 144, 152, 180, 195, 196, 228, 270, 558)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str,
                            help="Input file used to generate favicons")

    def handle(self, *args, **options):
        filename = options['filename']
        if not os.path.exists(filename):
            CommandError("File '%s' does not exist." % filename)
        # Save ICO
        img = Image.open(filename)
        output = os.path.join(settings.STATIC_DIR, 'favicon.ico')
        img.save(fp=output, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        # Save PNG
        for size in PNG_SIZE:
            img = Image.open(filename)
            output = os.path.join(settings.STATIC_DIR, 'favicon-%s.png' % size)
            img.thumbnail(size=(size, size), resample=Image.ANTIALIAS)
            img.save(output)
