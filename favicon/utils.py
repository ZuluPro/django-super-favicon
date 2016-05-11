"""Utilities for :mod:`favicon`."""
from django.utils.six import BytesIO, StringIO
from django.template import Context
from django.template.loader import get_template
from django.core.files import File
from PIL import Image

ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64)]
PNG_SIZES = (32, 57, 76, 96, 120, 128, 144, 152, 180, 195, 196, 228)
WINDOWS_PNG_SIZES = (
    ((128, 128), 'smalltile.png'),
    ((270, 270), 'mediumtile.png'),
    ((558, 270), 'widetile.png'),
    ((558, 558), 'largetile.png'),
)


def generate(source_file, storage, prefix=None, replace=False):
    """
    Creates favicons from a source file and upload into storage.
    This also create the ieconfig.xml file.

    :param source_file: File to use as string (local path) or filelike object
    :type source_file: str or file
    :param storage: Storage where upload files
    :type storage: :class:`django.core.files.storage.Storage`
    :param prefix: Prefix included in new files' names
    :type prefix: str
    :param replace: Delete file is already existing.
    :type replace: bool
    """
    prefix = prefix or ''

    def write_file(output_file, name, replace=False):
        """Upload to storage."""
        name = prefix + name
        if storage.exists(name):
            if replace:
                storage.delete(name)
            else:
                return
        content = File(output_file, name)
        storage._save(name, content)
    # Save ICO
    img = Image.open(source_file)
    output_file = BytesIO()
    img.save(fp=output_file, format='ICO', sizes=ICO_SIZES)
    write_file(output_file, 'favicon.ico')
    # Save PNG
    for size in PNG_SIZES:
        img = Image.open(source_file)
        output_file = BytesIO()
        output_name = 'favicon-%s.png' % size
        img.thumbnail(size=(size, size), resample=Image.ANTIALIAS)
        img.save(output_file, format='PNG')
        write_file(output_file, output_name)
    for size, output_name in WINDOWS_PNG_SIZES:
        img = Image.open(source_file)
        output_file = BytesIO()
        img.thumbnail(size=size, resample=Image.ANTIALIAS)
        img.save(output_file, format='PNG')
        write_file(output_file, output_name)
    # Create ieconfig.xml
    output_name = 'ieconfig.xml'
    output_file = StringIO()
    template = get_template('favicon/ieconfig.xml')
    output_content = template.render(Context({'tile_color': 'FFFFFF'}))
    output_file.write(output_content)
    write_file(output_file, 'ieconfig.xml')


def delete(storage, prefix=None):
    """
    Delete favicons from storage.

    :param storage: Storage where delete files
    :type storage: :class:`django.core.files.storage.Storage`
    :param prefix: Prefix included in files' names
    :type prefix: str
    """
    prefix = prefix or ''

    def delete_file(name):
        name = prefix + name
        storage.delete(name)

    delete_file('favicon.ico')
    for size in PNG_SIZES:
        name = 'favicon-%s.png' % size
        delete_file(name)
    for _, name in WINDOWS_PNG_SIZES:
        delete_file(name)
    delete_file('ieconfig.xml')
