from django import template

__author__ = 'nekmo'

register = template.Library()


def get_instance(element):
    return element.__module__ + '.' + element.__class__.__name__

register.filter('get_instance', get_instance)

@register.filter(name='isinstance')
def field_isinstance(element, compare):
    """Removes all values of arg from the given string"""
    instance_name = get_instance(element)
    return instance_name == compare