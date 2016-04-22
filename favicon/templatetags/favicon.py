from django import template
from django.template.loader import get_template

register = template.Library()


@register.simple_tag
def get_favicons():
    return get_template('favicon/favicon.html').render()
