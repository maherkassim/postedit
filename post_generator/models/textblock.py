from django.db import models
from post_generator.models import Post

class TextBlock(models.Model):
    post = models.ForeignKey(Post)
    
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=0,
    )
    
    text = models.CharField(
        'Text/Paragraph',
        max_length=1000,
    )
    
    printable = models.BooleanField(
        'Make this text block printable?',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.text
