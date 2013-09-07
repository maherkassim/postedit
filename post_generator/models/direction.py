from django.db import models
from post_generator.models.post import Post

class Direction(models.Model):
    post = models.ForeignKey(Post)
    tab_index = models.PositiveIntegerField()
    list_index = models.PositiveSmallIntegerField()
    english_text = models.CharField(max_length=250)
    somali_text = models.CharField(max_length=500, null=True, blank=True)
    french_text = models.CharField(max_length=500, null=True, blank=True)
    arabic_text = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english_text