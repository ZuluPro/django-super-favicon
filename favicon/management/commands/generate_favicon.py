import os

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
from django.core.files import File
from django.core.files.storage import get_storage_class
from django.utils.six import BytesIO

from PIL import Image
from favicon import settings

PNG_SIZE = (32, 57, 76, 96, 120, 128, 144, 152, 180, 195, 196)
WINDOWS_PNG_SIZE = (
    ([128, 128], 'smalltile.png'),
    ([270, 270], 'mediumtile.png'),
    ([558, 270], 'widetile.png'),
    ([558, 558], 'largetile.png'),
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str,
                            help="Input file used to generate favicons")

    def write_file(self, output_file, name):
        storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)
        content = File(output_file, name)
        storage.save(content)

    def handle(self, *args, **options):
        filename = options['filename']
        if not os.path.exists(filename):
            raise CommandError("File '%s' does not exist." % filename)
        # Set storage
        # Save ICO
        img = Image.open(filename)
        output_file = BytesIO()
        img.save(fp=output_file, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        self.write(output_file, 'favicon.ico')
        # Save PNG
        for size in PNG_SIZE:
            img = Image.open(filename)
            output_file = BytesIO()
            output_name = 'favicon-%s.png' % size
            img.thumbnail(size=(size, size), resample=Image.ANTIALIAS)
            img.save(output_file)
            self.write(output_file, output_name)
        for size, output_name in PNG_SIZE:
            img = Image.open(filename)
            output_file = BytesIO()
            img.thumbnail(size=size, resample=Image.ANTIALIAS)
            img.save(output_file)
            self.write(output_file, output_name)
        # Create ieconfig.xml
        output_name = 'ieconfig.xml'
        output_file = BytesIO()
        template = get_template('favicon/ieconfig.xml')
        output_content = template.render({'tile_color': 'FFFFFF'})
        output_file.write(output_content)
        self.write(output_file, 'ieconfig.xml')
