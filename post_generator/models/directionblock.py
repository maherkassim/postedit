from django.db import models
from post_generator.models import Post, DictionaryItem

class DirectionBlock(models.Model):
    post = models.ForeignKey(Post)
    header = models.ForeignKey(DictionaryItem)
    
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=0,
    )
    
    printable = models.BooleanField(
        'Make this block of directions printable?',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.header.english
