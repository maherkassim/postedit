from django.db import models

class Language(models.Model):
    full_name = models.CharField(max_length=20)
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.full_name