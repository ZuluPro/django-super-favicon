import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template
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
        for size, filename in PNG_SIZE:
            img = Image.open(filename)
            output = os.path.join(settings.STATIC_DIR, 'filename')
            img.thumbnail(size=size, resample=Image.ANTIALIAS)
            img.save(output)
        # Create ieconfig.xml
        output = os.path.join(settings.STATIC_DIR, 'ieconfig.xml')
        with open(output, 'w') as output_file:
            template = get_template('favicon/ieconfig.xml')
            output_content = template.render({'tile_color': 'FFFFFF'})
            output_file.write(output_content)
