"""Parameters for :mod:`favicon`."""
from django.conf import settings


STORAGE = getattr(settings, 'FAVICON_STORAGE', settings.STATICFILES_STORAGE)
STORAGE_OPTIONS = getattr(settings, 'FAVICON_STORAGE_OPTIONS', {})
PRECOMPOSED_BGCOLOR = getattr(settings, 'FAVICON_PRECOMPOSED_BG_COLOR', (255, 255, 255))
