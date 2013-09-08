from django.db import models
from post_generator.models.dictionaryitem import DictionaryItem
from post_generator.models.tab import Tab

class Header(models.Model):
    tab = models.ForeignKey(Tab)
    
    tab_index = models.PositiveIntegerField(
        'Tab Index',
    )
    
    text = models.ForeignKey(DictionaryItem)
    
    level = models.PositiveSmallIntegerField(
        'Header Level',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.text.english
