import json, operator, unicodedata, math

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from post_generator.models import Conversion, ConversionType, ConversionIngredient, Post, DictionaryItem

def convert(from_quant, from_units, from_type, to_units, to_type, grams_per_cup=0):
    """
    Conversion Calculator
    
    :param from_quant: Quantity of value to convert from
    :type from_quant: float
    :param from_units: DictionaryItem object ID
    :type from_units: int
    :param from_type: Type of value to convert from
    :type from_type: string: 'US' or 'Imperial' or 'Metric'
    :param to_units: DictionaryItem object ID
    :type to_units: int
    :param to_type: Type of value to convert to
    :type to_type: string: 'US' or 'Imperial' or 'Metric'
    :returns result: The converted quantity
    :rtype: str or float
    """
    
    if from_units == to_units and from_type == to_type:
        # Conversion is unnecessary, "from" and "to" are the same
        return from_quant
    
    # Retrieve Conversion objects for given units (DictionaryItem ID of Conversion object name)
    from_obj = Conversion.objects.get(name__id=from_units, unit_type__name__english=from_type)
    to_obj = Conversion.objects.get(name__id=to_units, unit_type__name__english=to_type)
    
    # If conversion is between different categories (eg. liquid -> weight),
    # pre-convert the given unit to the target unit based on the defined
    # grams_per_cup for the ingredient (stored in ConversionIngredient object)
    #  - Eg. Tablespoons -> Ounces => Tablespoons -> Cups -> Grams -> Ounces
    if from_obj.category.id != to_obj.category.id and grams_per_cup:
        
        # Retrieve cups and grams Conversion objects for use in conversion
        cups_obj = Conversion.objects.get(name__english="cup", unit_type__name__english='US')
        grams_obj = Conversion.objects.get(name__english="gram")
        
        # Convert and update the from_obj and from_quant to match the type of to_obj
        if from_obj.category.english == 'volume' and to_obj.category.english == 'weight':
            cups = convert(from_quant, from_obj, from_type, cups_obj, 'US')
            from_quant = cups * grams_per_cup
            from_obj = grams_obj
        elif from_obj.category.english == 'weight' and to_obj.category.english == 'volume':
            grams = convert(from_quant, from_obj.name.id, from_type, grams_obj.name.id, 'metric')
            from_quant = grams / grams_per_cup
            from_obj = cups_obj
        else:
            # Conversion was to occur between incompatible categories (eg. length -> weight)
            # Only compatible categories are Liquid and Weight
            # TODO: return error
            return ''
    elif from_obj.category.id != to_obj.category.id:
        # grams_per_cup was not defined, so conversion cannot be completed
        # TODO: return error
        return ''
    
    result = from_quant * from_obj.to_base / to_obj.to_base
    
    # Check if units are of the same type (ie. US/Imperial/Metric)
    if from_obj.unit_type.id != to_obj.unit_type.id:
        result = result * float(from_obj.unit_type.to_metric) / float(to_obj.unit_type.to_metric)
    return result

def parse_quantity(quantity):
    """
    Parse Quantity field of :model:`post_generator.Ingredient`
    
    :param quantity: Quantity as unicode string
    :type quantity: str or unicode
    :returns: Quantity as float
    :rtype: float
    """
    try:
        result = float(quantity)
    except ValueError:
        # Failure of float() indicates unicode characters (ie. fractions)
        # Note: this method assumes unicode (fraction) char is the last element
        #  - TODO: change method to handle other cases and check/validate inputs
        result = unicodedata.numeric(quantity[-1])
        if quantity[0:-1]:
            result += float(quantity[0:-1])
    return result

def update_conversion_ingredients(post_id):
    """
    Update or Create :model:`post_generator.ConversionIngredient` for :model:`post_generator.Ingredient' objects in a :model:`post_generator.Post`.
    
    Used to Auto-populate ConversionIngredient database for subsequent Lookups in :view:`post_generator.views.conversion.ingredient_intl_lookup`
    """
    post = Post.objects.get(pk=post_id)
    
    # Retrieve Cup and Gram DictionaryItem objects for use in conversion
    cups_obj = DictionaryItem.objects.get(english='cup')
    grams_obj = DictionaryItem.objects.get(english='gram')
    
    
    us_obj = ConversionType.objects.get(name__english='US')
    
    # Iterate through all IngredientBlocks associated with the newly updated Post object
    for ingredient_block in post.ingredientblock_set.all():
        
        # Iterate through the Ingredients in each IngredientBlock
        for ingredient in ingredient_block.ingredient_set.all():
            
            # Only check g<->cup conversion rate if intl and quantity (and units) are specified
            if ingredient.intl and ingredient.intl_units and \
               ingredient.quantity and ingredient.quantity_units:
                
                # Retrieve Quantity Units Conversion object
                try:
                    # US is preferred type for Quantity Units, but Imperial is possible (usually for weight)
                    quant_obj = Conversion.objects.get(name__id=ingredient.quantity_units.id, unit_type__name__english='US')
                except Conversion.DoesNotExist:
                    try:
                        quant_obj = Conversion.objects.get(name__id=ingredient.quantity_units.id, unit_type__name__english='imperial')
                    except Conversion.DoesNotExist:
                        # Quantity Units specified does not yet have a corresponding Conversion object
                        # TODO: display an error
                        continue
                
                # Retrieve Intl Units Conversion object
                try:
                    # Metric is the only type used for Intl Units
                    intl_obj = Conversion.objects.get(name__id=ingredient.intl_units.id, unit_type__name__english='metric')
                except Conversion.DoesNotExist:
                    # Intl Units specified does not yet have a corresponding Conversion object
                    # TODO: display an error
                    continue
                
                volume_obj = DictionaryItem.objects.get(english='volume')
                weight_obj = DictionaryItem.objects.get(english='weight')
                
                # Check that valid categories are being used to convert
                valid_conversion = False
                if quant_obj.category.id == volume_obj.id and \
                   intl_obj.category.id == weight_obj.id:
                    
                    # Convert volume to cups and weight to grams
                    cups = convert(parse_quantity(ingredient.quantity), ingredient.quantity_units.id, quant_obj.unit_type.name.english, cups_obj.id, 'US')
                    grams = convert(float(ingredient.intl), ingredient.intl_units.id, intl_obj.unit_type.name.english, grams_obj.id, 'metric')
                    valid_conversion = True
                
                elif quant_obj.category.id == weight_obj.id and \
                     intl_obj.category.id == volume_obj.id:
                    
                    # Convert volume to cups and weight to grams
                    cups = convert(float(ingredient.intl), ingredient.intl_units.id, intl_obj.unit_type.name.english, cups_obj.id, 'US')
                    grams = convert(parse_quantity(ingredient.quantity), ingredient.quantity_units.id, quant_obj.unit_type.name.english, grams_obj.id, 'metric')
                    valid_conversion = True
                
                if valid_conversion:
                    grams_per_cup = grams / cups
                    
                    # Retrieve or create a ConversionIngredient object for the ingredient
                    ing_set = ConversionIngredient.objects.filter(name__id=ingredient.name.id)
                    if ingredient.size:
                        ing_set.filter(size__id=ingredient.size.id)
                    for style in ingredient.prep_style.all():
                        ing_set.filter(prep_style__id=style.id)
                    
                    if ing_set: # Existing ConversionIngredient found
                        conv_ing = ing_set[0]
                    else: # Create new ConversionIngredient
                        conv_ing = ConversionIngredient(name=ingredient.name, grams_per_cup=0)
                        conv_ing.save()
                        for prep_style in ingredient.prep_style.all():
                            conv_ing.prep_style.add(prep_style)
                        if ingredient.size:
                            conv_ing.size = ingredient.size
                    
                    # Save the ConversionIngredient with the new grams_per_cup
                    conv_ing.grams_per_cup = grams_per_cup
                    conv_ing.save()

@login_required
@csrf_exempt
def ingredient_intl_lookup(request):
    """
    Automatically calculates Intl field of :model:`post_generator.Ingredient`.
    
    Requires:
    
    - compatible input for convert function above
    - grams_per_cup if one unit is volume and the other is weight (auto-populated by :view:`post_generator.views.conversion.update_conversion_ingredients` if previously entered)
    
    :returns response: JSON HttpReponse (for use with AJAX in :model:`post_generator.Post` form)
    :rtype: HttpResponse
    """
    
    intl = ''
    if request.method == 'POST' and request.is_ajax():
        # TODO: add cases to handle non-AJAX or GET requests
        
        # Read in POST data
        quantity = request.POST['quantity']
        quantity_units = request.POST['quantity_units']
        intl_units = request.POST['intl_units']
        size=request.POST['size']
        styles = request.POST.getlist('styles')
        
        if quantity and quantity_units and intl_units:
            # Filter for the desired ConversionIngredient object
            ing_set = ConversionIngredient.objects.filter(name__id=request.POST['name'])
            if size:
                ing_set = ing_set.objects.filter(size__id=size)
            for style in styles:
                if style:
                    ing_set = ing_set.filter(prep_style__id=style)
            
            # If a matching object was found, 
            if ing_set:
                conv_ing = ing_set[0]
            
            # Determine Quantity Units type (US/Imperial)
            error_occurred = False
            try:
                # US is preferred type for Quantity Units, but Imperial is possible (usually for weight)
                Conversion.objects.get(name__id=quantity_units, unit_type__name__english='US')
                quantity_type = 'US'
            except Conversion.DoesNotExist:
                try:
                    Conversion.objects.get(name__id=quantity_units, unit_type__name__english='imperial')
                    quantity_type = 'imperial'
                except Conversion.DoesNotExist:
                    # Quantity Units specified does not yet have a corresponding Conversion object
                    # TODO: display an error
                    error_occurred = True
            
            # Determine Intl Units type (Metric)
            try:
                Conversion.objects.get(name__id=intl_units, unit_type__name__english='metric')
                intl_type = 'metric'
            except Conversion.DoesNotExist:
                # Intl Units specified does not yet have a corresponding Conversion object
                # TODO: display an error
                error_occurred = True
                            
            if not error_occurred:               
                if ing_set and conv_ing.grams_per_cup:
                    intl = convert(parse_quantity(quantity),
                                   quantity_units,
                                   quantity_type,
                                   intl_units,
                                   intl_type,
                                   float(conv_ing.grams_per_cup))
                else:
                    intl = convert(parse_quantity(quantity),
                                   quantity_units,
                                   quantity_type,
                                   intl_units,
                                   intl_type)
    if intl:
        # If there haven't been any errors (invalid input or request type),
        # do some post-processing on the calculated value:
        #   - Display conversions from teaspoons to milliliters to the nearest 1/4
        #      - If the value is not too large (eg. < 100)
        quant_units_obj = DictionaryItem.objects.get(pk=quantity_units)
        intl_units_obj = DictionaryItem.objects.get(pk=intl_units)
        
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
    return HttpResponse(json.dumps({'intl':intl}), content_type='application/json')

