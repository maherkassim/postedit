from django.db import models
from post_generator.models.dictionaryitem import DictionaryItem
from post_generator.models.post import Post
from post_generator.models.header import Header

class Ingredient(models.Model):
    post = models.ForeignKey(Post)
    
    header = models.ForeignKey(Header)
    
    name = models.ForeignKey(
        DictionaryItem,
        related_name="name",
    )
    
    size = models.ForeignKey(
        DictionaryItem,
        related_name="size",
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
        blank=True,
    )
    
    prep_style = models.ForeignKey(
        DictionaryItem,
        related_name="prep_style",
        verbose_name="Preparation/Style",
        blank=True,
    )
    
    english_comment = models.CharField(
        'English Comment',
        max_length=250,
        blank=True,
    )
    
    somali_comment = models.CharField(
        'Somali Comment',
        max_length=250,
        blank=True,
    )
    
    french_comment = models.CharField(
        'French Comment',
        max_length=250,
        blank=True,
    )
    
    arabic_comment = models.CharField(
        'Arabic Comment',
        max_length=250,
        blank=True,
    )
    
    optional = models.BooleanField()
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.name.english
