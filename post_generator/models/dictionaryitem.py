from django.db import models

class DictionaryItem(models.Model):
    english = models.CharField(max_length=250)
    english_plural = models.CharField(max_length=250, null=True, blank=True)
    somali = models.CharField(max_length=250, null=True, blank=True)
    french = models.CharField(max_length=250, null=True, blank=True)
    french_plural = models.CharField(max_length=250, null=True, blank=True)
    french_male = models.NullBooleanField()
    arabic = models.CharField(max_length=250, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english