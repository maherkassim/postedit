from django.db import models
from post_generator.models.dictionaryitem import DictionaryItem

class Post(models.Model):
    link = models.URLField()
    title = models.ForeignKey(DictionaryItem)
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.title.english