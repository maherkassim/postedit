from django.db import models
from post_generator.models.post import Post

class Video(models.Model):
    post = models.ForeignKey(Post)
    
    tab_index = models.PositiveIntegerField(
        'Tab Index',
    )
    
    link = models.URLField(
        'Video URL',
    )
    
    width = models.PositiveSmallIntegerField(
        'Video Width',
    )
    
    height = models.PositiveSmallIntegerField(
        'Video Height',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link
