from django.db import models
from post_generator.models import DictionaryItem, IngredientBlock, TextBlock

class Ingredient(models.Model):
    ingredient_block = models.ForeignKey(IngredientBlock)
    
    name = models.ForeignKey(
        DictionaryItem,
        related_name="name",
    )
    
    size = models.ForeignKey(
        DictionaryItem,
        related_name="size",
        null=True,
        blank=True,
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
    )
    
    prep_style = models.ForeignKey(
        DictionaryItem,
        related_name="prep_style",
        verbose_name="Preparation Methods/Styles",
        null=True,
        blank=True,
    )
    
    comment = models.ForeignKey(
        TextBlock,
        related_name="comment",
        null=True,
        blank=True,
    ) 
    
    optional = models.BooleanField()
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.ingredient_block.post.title.english.title() + ' - ' + self.ingredient_block.header.english.title() + ' - ' + self.name.english
