from django import template
from django.template.loader import get_template
from django.core.files.storage import get_storage_class
from .. import settings

register = template.Library()


@register.simple_tag
def get_favicons(prefix=None):
    """
    Generate HTML to include in headers for get all favicons url.

    :param prefix: Prefix of files' names
    :type prefix: str
    :return: HTML link and meta
    :rtype: str
    """
    return get_template('favicon/favicon.html').render({
        'prefix': prefix
    })


@register.simple_tag
def favicon_url(filename, prefix=None):
    """
    Generate URL for find a single file. It uses :meth:`url()` of storage
    defined in ``settings.FAVICON_STORAGE``.

    :param filename: Filename
    :type filename: str
    :param prefix: Prefix of filename
    :type prefix: str
    :return: File's URL
    :rtype: str
    """
    storage = get_storage_class(settings.STORAGE)(**settings.STORAGE_OPTIONS)
    prefix = prefix or ''
    name = prefix + filename
    return storage.url(name)
