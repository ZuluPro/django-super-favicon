import os
from django.core.files.storage import Storage

TEST_DIR = os.path.dirname(__file__)
BASE_IMG = os.path.join(TEST_DIR, 'logo.png')
BASE_URL = 'https://example.com/'

EXPECTED_FILES = (
    'favicon.ico',
    'ieconfig.xml',
    'smalltile.png', 'mediumtile.png', 'largetile.png', 'widetile.png',
    'favicon-32.png', 'favicon-57.png', 'favicon-76.png', 'favicon-96.png',
    'favicon-120.png', 'favicon-128.png', 'favicon-144.png', 'favicon-152.png',
    'favicon-180.png', 'favicon-195.png', 'favicon-196.png', 'favicon-228.png',
)


class handled_files(dict):
    """
    Dict for gather information about fake storage and clean between tests.
    You should use the constant instance ``HANDLED_FILES`` and clean it
    before tests.
    """
    def __init__(self):
        super(handled_files, self).__init__()
        self.clean()

    def clean(self):
        self['written_files'] = {}
        self['deleted_files'] = {}
HANDLED_FILES = handled_files()


class FakeStorage(Storage):
    def _save(self, name, content):
        HANDLED_FILES['written_files'][name] = content

    def _open(self, name, mode='rb'):
        HANDLED_FILES['written_files'][name].seek(0)
        return HANDLED_FILES['written_files'][name]

    def exists(self, name):
        return name in HANDLED_FILES['written_files'].keys()

    def delete(self, name):
        fi = HANDLED_FILES['written_files'].pop(name, None)
        if fi:
            HANDLED_FILES['deleted_files'][name] = fi

    def post_process(self):
        pass

    def url(self, name):
        return BASE_URL + name
