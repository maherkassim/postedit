from django.db import models
from post_generator.models.post import Post
from post_generator.models.tab import Tab

class TextBlock(models.Model):
    post = models.ForeignKey(Post)
    post_intro = models.BooleanField()
    tab = models.ForeignKey(Tab)
    tab_index = models.PositiveIntegerField()
    text = models.CharField(max_length=1000)
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.text