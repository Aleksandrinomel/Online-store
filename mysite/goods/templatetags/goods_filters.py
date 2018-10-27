from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter


def make_list_2(value):
    return value.split(',')[0]

register.filter('make_list_2', make_list_2)