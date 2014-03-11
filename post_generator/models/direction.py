from django.db import models
from post_generator.models import DirectionBlock

class Direction(models.Model):
    direction_block = models.ForeignKey(DirectionBlock)
    
    item_number = models.PositiveIntegerField(
        'Index in set of directions',
    )
    
    english = models.CharField(
        'English Direction',
        max_length=250,
    )
    
    somali = models.CharField(
        'Somali Direction',
        max_length=500,
        blank=True,
    )
    
    french = models.CharField(
        'French Direction',
        max_length=500,
        blank=True,
    )
    
    arabic = models.CharField(
        'Arabic Direction',
        max_length=500,
        blank=True,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.direction_block.post.title.english.title() + ' - ' + \
               self.direction_block.header.english.title() + ' - ' + \
               str(self.item_number) + '. ' + self.english
