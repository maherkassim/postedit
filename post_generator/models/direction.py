from django.db import models
from post_generator.models.post import Post

class Direction(models.Model):
    post = models.ForeignKey(Post)
    
    tab_index = models.PositiveIntegerField(
        'Tab Index',
    )
    
    list_index = models.PositiveSmallIntegerField(
        'Direction List Index',
    )

    english_text = models.CharField(
        'English Direction',
        max_length=250,
    )
    
    somali_text = models.CharField(
        'Somali Direction',
        max_length=500,
        blank=True,
    )
    
    french_text = models.CharField(
        'French Direction',
        max_length=500,
        blank=True,
    )

    arabic_text = models.CharField(
        'Arabic Direction',
        max_length=500,
        blank=True,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english_text
