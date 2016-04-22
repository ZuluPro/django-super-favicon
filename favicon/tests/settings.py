SECRET_KEY = '&qaeg(mBecauseitsmandatoryv@@n$if67ba-4e9&kk+j$$c+'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'favicon',
]

STATIC_URL = '/static/'
FAVICON_STORAGE = 'favicon.tests.utils.FakeStorage'
