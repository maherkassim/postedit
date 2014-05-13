from django.db import models
from post_generator.models import DictionaryItem, IngredientBlock, TextBlock

class Ingredient(models.Model):
    ingredient_block = models.ForeignKey(IngredientBlock)
    
    name = models.ForeignKey(
        DictionaryItem,
        related_name="name",
        limit_choices_to={'_set':'General'},
    )
    
    size = models.ForeignKey(
        DictionaryItem,
        related_name="size",
        null=True,
        blank=True,
        limit_choices_to={'_set':'Size'},
    )
    
    quantity = models.CharField(
        'Quantity',
        max_length=20,
        blank=True,
    )
    
    quantity_units = models.ForeignKey(
        DictionaryItem,
        related_name="quantity_units",
        null=True,
        blank=True,
        limit_choices_to={'_set':'Quant_Unit'},
    )
    
    intl = models.CharField(
        'International Quantity',
        max_length=20,
        blank=True,
    )
    
    intl_units = models.ForeignKey(
        DictionaryItem,
        related_name="intl_units",
        verbose_name="International Units",
        null=True,
        blank=True,
        limit_choices_to={'_set':'Intl_Unit'},
    )
    
    prep_style = models.ManyToManyField(
        DictionaryItem,
        related_name='prep_style',
        verbose_name='Preparation Methods/Styles',
        null=True,
        blank=True,
        limit_choices_to={'_set':'Prep_Type'},
    )
    
    english = models.CharField(
        'English Comment',
        max_length=1000,
        blank=True,
    )
    
    somali = models.CharField(
        'Somali Comment',
        max_length=1000,
        blank=True,
    )
    
    french = models.CharField(
        'French Comment',
        max_length=1000,
        blank=True,
    )
    
    arabic = models.CharField(
        'Arabic Comment',
        max_length=1000,
        blank=True,
    )
    
    optional = models.BooleanField()
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return unicode((str(self.quantity) or '') + ' ' + (str(self.quantity_units) or '') + ' (' + (str(self.intl) or '') + ' ' + (str(self.intl_units) or '') + ') ' + (str(self.size) or '') + ' ' + self.name.english)
