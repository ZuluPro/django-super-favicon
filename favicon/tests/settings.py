SECRET_KEY = '&qaeg(mBecauseitsmandatoryv@@n$if67ba-4e9&kk+j$$c+'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'favicon',
]

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp'
FAVICON_STORAGE = 'favicon.tests.utils.FakeStorage'
