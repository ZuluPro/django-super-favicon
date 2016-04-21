from django.conf import settings


STORAGE = getattr(settings, 'FAVICON_STORAGE', settings.DEFAULT_FILE_STORAGE)
STORAGE_OPTIONS = getattr(settings, 'FAVICON_STORAGE_OPTIONS', {})
