import unicodedata
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

@register.filter(name='set_field')
def set_field(item):
    return item['_set']

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

def get_plural(dictionary, lang, gender=''):
  if dictionary:
    if lang == 'english':
      return dictionary.english_plural or dictionary.english
    elif lang == 'french':
      if gender == 'masculine':
        return dictionary.french_masculine_plural or dictionary.french
      elif gender == 'feminine':
        return dictionary.french_feminine_plural or dictionary.french_feminine
      else:
        return dictionary.french_masculine_plural or dictionary.french_feminine_plural \
         or dictionary.french or dictionary.french_feminine
    else:
      return dictionary.__dict__[lang]

def get_single(dictionary, lang, gender=''):
   if dictionary:
    if lang == 'french':
      if gender == 'masculine':
        return dictionary.french
      elif gender == 'feminine':
        return dictionary.french_feminine
      else:
        return dictionary.french or dictionary.french_feminine
    else:
      return dictionary.__dict__[lang]

@register.filter(name='ing_name')
def ing_name(ing, lang):
  quant = ing.quantity
  intl = ing.intl
  comment = ing.__dict__[lang]
  gender = 'masculine' if ing.name.french else 'feminine'
  if unicodedata.numeric(quant) > 1:
    quant_units = get_plural(ing.quantity_units, lang)
    intl_units = get_plural(ing.intl_units, lang)
    size = get_plural(ing.size, lang, gender)
    name = get_plural(ing.name, lang)
    style = ", ".join(map(lambda style: get_plural(style, lang, gender), ing.prep_style.all()))
  else:
    quant_units = get_single(ing.quantity_units, lang)
    intl_units = get_single(ing.intl_units, lang)
    size = get_single(ing.size, lang, gender)
    style = ", ".join(map(lambda style: get_plural(style, lang, gender), ing.prep_style.all()))
    if quant_units:
      name = get_plural(ing.name, lang)
    else:
      name = get_single(ing.name, lang)

  result = []
  if quant: result.append(quant)
  if quant_units: result.append(quant_units)
  if intl: result.append('(' + intl + ' ' + intl_units + ')')
  if size and (lang == 'english' or lang == 'french'): result.append(size)
  result.append(name)
  if size and (lang == 'somali' or lang == 'arabic'): result.append(size)
  if style: result.append('(' + style + ')')
  if comment: result.append('- ' + comment)
  return " ".join(result)

