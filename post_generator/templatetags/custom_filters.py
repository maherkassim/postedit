from django import template

register = template.Library()

@register.filter(name='dict_val')
def dict_val(dictionary, key):
    return dictionary.__dict__[key]

@register.filter(name='get_loc')
def get_loc(block):
    return block['_loc_index'].value

@register.filter(name='loc_field')
def loc_field(block):
    return block['_loc_index']

@register.filter(name='tab_field')
def tab_field(block):
    return block['_tabbed']

@register.filter(name='class_name')
def class_name(value):
  return value.__class__.__name__

@register.filter(name='model_name')
def model_name(value):
  return value._meta.model._meta.model_name

@register.filter(name='scale')
def scale(value):
  if value:
    return int(value)/4

@register.filter(name='or_blank')
def or_blank(value):
  return value or ''


