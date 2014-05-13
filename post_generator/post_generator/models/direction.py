from django.db import models
from post_generator.models import DirectionBlock

class Direction(models.Model):
    direction_block = models.ForeignKey(DirectionBlock)
    
    english = models.TextField(
        'English Direction',
    )
    
    somali = models.TextField(
        'Somali Direction',
        blank=True,
    )
    
    french = models.TextField(
        'French Direction',
        blank=True,
    )
    
    arabic = models.TextField(
        'Arabic Direction',
        blank=True,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return unicode(self.english)
