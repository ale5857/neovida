from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def url_if_exists(name, *args):
    try:
        return reverse(name, args=args)
    except NoReverseMatch:
        return "#"
    