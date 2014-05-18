import json, operator, unicodedata, math

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from post_generator.models import Conversion, ConversionType, ConversionIngredient, Post, DictionaryItem

def convert(from_quant, from_units, from_type, to_units, to_type, grams_per_cup=0):
    if from_units == to_units and from_type == to_type:
        return from_quant
    
    from_obj = Conversion.objects.get(name__id=from_units, unit_type__name__english=from_type)
    to_obj = Conversion.objects.get(name__id=to_units, unit_type__name__english=to_type)
    
    if from_obj.category.id != to_obj.category.id and grams_per_cup:
        cups_obj = Conversion.objects.get(name__english="cup", unit_type__name__english='US')
        grams_obj = Conversion.objects.get(name__english="gram")
        if from_obj.category.english == 'volume' and to_obj.category.english == 'weight':
            cups = convert(from_quant, from_obj, from_type, cups_obj, 'US')
            from_quant = cups * grams_per_cup
            from_obj = grams_obj
        elif from_obj.category.english == 'weight' and to_obj.category.english == 'volume':
            grams = convert(from_quant, from_obj, from_type, grams_obj, 'Metric')
            from_quant = grams / grams_per_cup
            from_obj = cups_obj
        else:
            return ''
    elif from_obj.category.id != to_obj.category.id:
        return ''
    
    result = from_quant * from_obj.to_base / to_obj.to_base
    # Check if units are of the same type (ie. US/Imperial/Metric)
    if from_obj.unit_type.id != to_obj.unit_type.id:
        result = result * float(from_obj.unit_type.to_metric) / float(to_obj.unit_type.to_metric)
    return result

def parse_quantity(quantity):
    try:
        result = float(quantity)
    except ValueError:
        result = unicodedata.numeric(quantity[-1])
        if quantity[0:-1]:
            result += float(quantity[0:-1])
    return result

def UpdateConversionIngredients(post_id):
    post = Post.objects.get(pk=post_id)
    cups_obj = DictionaryItem.objects.get(english='cup')
    us_obj = ConversionType.objects.get(name__english='US')
    for ingredient_block in post.ingredientblock_set.all():
        for ingredient in ingredient_block.ingredient_set.all():
            if ingredient.intl_units and ingredient.quantity_units:
                from_obj = Conversion.objects.get(name__id=ingredient.quantity_units.id, unit_type__name__english='US')
                to_obj = Conversion.objects.get(name__id=ingredient.intl_units.id, unit_type__name__english='Metric')
                if ingredient.intl and from_obj.category.id != to_obj.category.id:
                    cups = convert(parse_quantity(ingredient.quantity), ingredient.quantity_units.id, 'US', cups_obj.id, 'US')
                    grams_per_cup = float(ingredient.intl) / cups
                    
                    ing_set = ConversionIngredient.objects.filter(name__id=ingredient.name.id)
                    if ingredient.size:
                        ing_set.filter(size__id=ingredient.size.id)
                    for style in ingredient.prep_style.all():
                        ing_set.filter(prep_style__id=style.id)
                    if ing_set:
                        conv_ing = ing_set[0]
                    else:
                        conv_ing = ConversionIngredient(name=ingredient.name, grams_per_cup=0)
                        conv_ing.save()
                        for prep_style in ingredient.prep_style.all():
                            conv_ing.prep_style.add(prep_style)
                        if ingredient.size:
                            conv_ing.size = ingredient.size
                    conv_ing.grams_per_cup = grams_per_cup
                    conv_ing.save()

@login_required
@csrf_exempt
def IngredientIntlLookup(request):
    intl = ''
    if request.method == 'POST' and request.is_ajax():
        quantity = request.POST['quantity']
        quantity_units = request.POST['quantity_units']
        intl_units = request.POST['intl_units']
        ing_set = ConversionIngredient.objects.filter(name__id=request.POST['name'])
        
        size=request.POST['size']
        if size:
            ing_set = ing_set.objects.filter(size__id=size)
        
        for style in request.POST.getlist('styles'):
            if style:
                ing_set = ing_set.filter(prep_style__id=style)
        
        if ing_set:
           ing = ing_set[0]
           if quantity and quantity_units and intl_units and ing.grams_per_cup:
               intl = convert(parse_quantity(quantity), quantity_units, 'US', intl_units, 'metric', float(ing.grams_per_cup))
        if quantity and quantity_units and intl_units and not intl:
            intl = convert(parse_quantity(quantity), quantity_units, 'US', intl_units, 'metric')
    quant_units_obj = DictionaryItem.objects.get(pk=quantity_units)
    intl_units_obj = DictionaryItem.objects.get(pk=intl_units)
    if intl:
        if intl < 100 and quant_units_obj.english == 'teaspoon' and intl_units_obj.english == 'milliliter':
            to_two = round(intl, 2)
            to_zero = math.floor(to_two)
            dec = to_two - to_zero
            if dec < 0.125:
              intl = to_zero
            elif dec < 0.375:
              intl = to_zero + 0.25
            elif dec < 0.625:
              intl = to_zero + 0.5
            elif dec < 0.875:
              intl = to_zero + 0.75
            else:
              intl = round(intl)
        else:
            intl = round(intl)
    data = json.dumps({'intl':intl})
    return HttpResponse(data, content_type='application/json')

