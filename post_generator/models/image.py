from django.db import models
from post_generator.models.post import Post

class Image(models.Model):
    tab_index = models.PositiveIntegerField(
        'Tab Index',
        null=True,
        blank=True,
    )
    
    post = models.ForeignKey(Post)
    
    post_main = models.BooleanField(
        'Main Image in Post?',
    )
    
    link = models.URLField(
        'Image URL',
    )
    
    wordpress_image_id = models.PositiveIntegerField(
        'WordPress Image ID (where applicable)',
        null=True,
        blank=True,
    )
    
    width = models.PositiveSmallIntegerField(
        'Image Width',
    )
    
    height = models.PositiveSmallIntegerField(
        'Image Height',
    )
    
    english_caption = models.CharField(
        'English Caption',
        max_length=250,
        blank=True,
    )
    
    somali_caption = models.CharField(
        'Somali Caption',
        max_length=250,
        blank=True,
    )
    
    french_caption = models.CharField(
        'French Caption',
        max_length=250,
        blank=True,
    )
    
    arabic_caption = models.CharField(
        'Arabic Caption',
        max_length=250,
        blank=True,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link
