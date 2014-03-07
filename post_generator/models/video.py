from django.db import models
from post_generator.models import Post

class Video(models.Model):
    post = models.ForeignKey(Post)
    
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=0,
    )
    
    link = models.URLField(
        'Video URL',
    )
    
    width = models.PositiveSmallIntegerField(
        'Video Width',
        default=810,
    )
    
    height = models.PositiveSmallIntegerField(
        'Video Height',
        default=456,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link
