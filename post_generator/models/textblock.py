from django.db import models
from post_generator.models import Post

class TextBlock(models.Model):
    post = models.ForeignKey(Post)
    
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=-1,
    )
    
    _tabbed = models.BooleanField(
        default=True,
    )
    
    english = models.TextField(
        'English Text/Paragraph',
    )
    
    french = models.TextField(
        'French Text/Paragraph',
        blank=True,
    )
    
    somali = models.TextField(
        'Somali Text/Paragraph',
        blank=True,
    )
    
    arabic = models.TextField(
        'Arabic Text/Paragraph',
        blank=True,
    )

    printable = models.BooleanField(
        'Make this text block printable?',
    )
    
    header = models.BooleanField(
        'Is this text a header?',
        default = False,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english
