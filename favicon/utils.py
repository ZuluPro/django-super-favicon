from django.utils.six import BytesIO
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


def generate(source_file, storage):
    def write_file(output_file, name):
        content = File(output_file, name)
        storage._save(content, name)
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
    output_file = BytesIO()
    template = get_template('favicon/ieconfig.xml')
    output_content = template.render({'tile_color': 'FFFFFF'})
    output_file.write(output_content)
    write_file(output_file, 'ieconfig.xml')


def delete(storage):
    storage.delete('favicon.ico')
    for size in PNG_SIZES:
        name = 'favicon-%s.png' % size
        storage.delete(name)
    for _, name in WINDOWS_PNG_SIZES:
        storage.delete(name)
    storage.delete('ieconfig.xml')
