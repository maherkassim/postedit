from django.db import models

class Language(models.Model):
    name = models.CharField(
        'Language Name',
        max_length=20,
    )
    
    display_name = models.CharField(
        'Language Name (for display eg. post tab titles)',
        max_length=20,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.display_name
