from django import template

register = template.Library()

@register.filter(name='dict_val')
def dict_val(dictionary, key):
    # Retrieves value in dictionary for the given key
    return dictionary.__dict__[key]


@register.filter(name='class_name')
def class_name(value):
  return value.__class__.__name__
