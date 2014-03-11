from django.db import models
from post_generator.models import Post

class TextBlock(models.Model):
    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
    )
    
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=-1,
    )
    
    _tabbed = models.BooleanField(
        default=True,
    )
    
    english = models.CharField(
        'English Text/Paragraph',
        max_length=1000,
    )
    
    french = models.CharField(
        'French Text/Paragraph',
        max_length=1000,
        blank=True,
    )
    
    somali = models.CharField(
        'Somali Text/Paragraph',
        max_length=1000,
        blank=True,
    )
    
    arabic = models.CharField(
        'Arabic Text/Paragraph',
        max_length=1000,
        blank=True,
    )
    
    printable = models.BooleanField(
        'Make this text block printable?',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english
