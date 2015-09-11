from django import template

__author__ = 'nekmo'

register = template.Library()


@register.filter(name='isinstance')
def field_isinstance(element, compare):
    """Removes all values of arg from the given string"""
    instance_name = element.__module__ + '.' + element.__class__.__name__
    return instance_name == compare