from django import template
from django.template.loader import get_template
from django.core.files.storage import get_storage_class
from .. import settings

register = template.Library()


@register.simple_tag
def get_favicons(prefix=None):
    """Display all needed headers."""
    return get_template('favicon/favicon.html').render({
        'prefix': prefix
    })


@register.simple_tag
def favicon_url(filename, prefix=None):
    storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)
    prefix = prefix or ''
    name = prefix + filename
    return storage.url(name)
