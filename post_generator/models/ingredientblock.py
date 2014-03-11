from django.db import models
from post_generator.models import Post, DictionaryItem

class IngredientBlock(models.Model):
    post = models.ForeignKey(Post)
    header = models.ForeignKey(DictionaryItem)
 
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=-1,
    )
    
    _tabbed = models.BooleanField(
        default=True,
    )
    
    printable = models.BooleanField(
        'Make this block of ingredients printable?',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.header.english
