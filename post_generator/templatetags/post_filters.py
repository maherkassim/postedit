from django import template

register = template.Library()

@register.filter(name='contains')
def contains(value,arg):
    return value in arg
