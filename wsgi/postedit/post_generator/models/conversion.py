from django.db import models
from post_generator.models import DictionaryItem

class ConversionType(models.Model):
    name = models.ForeignKey(
        DictionaryItem,
        related_name="conv_name",
        limit_choices_to={'_set':'Conv_Type'},
    )
    
    to_metric = models.FloatField(
        "Converted to Metric",
    )

    category = models.ForeignKey(
        DictionaryItem,
        related_name="type_category",
        limit_choices_to={'_set':'Conv_Cat'},
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return unicode(self.name.english) + ' (' + unicode(self.category.english) + ')'

class Conversion(models.Model):
    name = models.ForeignKey(
        DictionaryItem,
        related_name="unit_name",
    )
    
    unit_type = models.ForeignKey(
         ConversionType,
         related_name="unit_type",
    )
    
    to_base = models.FloatField(
        "Amount of base unit (eg. 3 Teaspoons in a Tablespoons)",
    )
    
    category = models.ForeignKey(
        DictionaryItem,
        related_name="category",
        limit_choices_to={'_set':'Conv_Cat'},
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return unicode(self.name.english)

class ConversionIngredient(models.Model):
    name = models.ForeignKey(
        DictionaryItem,
        related_name="ingredient_name",
        limit_choices_to={'_set':'General'},
    )
    
    size = models.ForeignKey(
        DictionaryItem,
        related_name="ingredient_size",
        null=True,
        blank=True,
        limit_choices_to={'_set':'Size'},
    )
    
    prep_style = models.ManyToManyField(
        DictionaryItem,
        related_name='ingredient_style',
        verbose_name='Preparation Methods/Styles',
        null=True,
        blank=True,
        limit_choices_to={'_set':'Prep_Type'},
    )
    
    grams_per_cup = models.FloatField(
        "Grams per Cup",
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        result = self.name.english
        if self.size:
            result = self.size.english + ' ' + result
        return unicode(result)
