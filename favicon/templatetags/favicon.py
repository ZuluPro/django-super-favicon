from django import template
from django.template.loader import get_template

register = template.Library()


@register.simple_tag
def get_favicons():
    """Display all needed headers."""
    return get_template('favicon/favicon.html').render()
