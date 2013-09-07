from django.db import models
from post_generator.models.post import Post

class Video(models.Model):
    tab_index = models.PositiveIntegerField()
    post = models.ForeignKey(Post)
    link = models.URLField()
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link