from django.db import models
from post_generator.models import Post

class Image(models.Model):
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=0,
    )
    
    post = models.ForeignKey(Post)
    
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
        default=820,
    )
    
    height = models.PositiveSmallIntegerField(
        'Image Height',
        default=543,
    )
    
    english_caption = models.CharField(
        'English Caption',
        max_length=250,
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
