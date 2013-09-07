from django.db import models
from post_generator.models.post import Post

class Image(models.Model):
    tab_index = models.PositiveIntegerField(null=True, blank=True)
    post = models.ForeignKey(Post)
    post_main = models.BooleanField()
    link = models.URLField()
    wordpress_image_id = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    english_caption = models.CharField(max_length=250, null=True, blank=True)
    somali_caption = models.CharField(max_length=250, null=True, blank=True)
    french_caption = models.CharField(max_length=250, null=True, blank=True)
    arabic_caption = models.CharField(max_length=250, null=True, blank=True)
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link