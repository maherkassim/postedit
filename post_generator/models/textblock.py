from django.db import models
from post_generator.models.post import Post
from post_generator.models.tab import Tab

class TextBlock(models.Model):
    post = models.ForeignKey(Post)
    
    post_intro = models.BooleanField(
        'Introduction Paragraph?',
    )
    
    tab = models.ForeignKey(Tab)
    
    tab_index = models.PositiveIntegerField(
        'Tab Index',
    )
    
    text = models.CharField(
        'Text/Paragraph',
        max_length=1000,
    )
    
    printable = models.BooleanField(
    	'Add to print option?',	
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.text
