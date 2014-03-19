from django.db import models
from post_generator.models import Post

class Image(models.Model):
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=-1,
    )
    
    _tabbed = models.BooleanField(
        default=True,
    )
    
    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
    )
    
    english = models.CharField(
        'English Caption',
        max_length=1000,
    )

    somali = models.CharField(
        'Somali Caption',
        max_length=1000,
        blank=True,
    )

    french = models.CharField(
        'French Caption',
        max_length=1000,
        blank=True,
    )
    
    arabic = models.CharField(
        'Arabic Caption',
        max_length=1000,
        blank=True,
    )
   
    link = models.URLField(
        'Image URL',
    )
    
    wordpress_image_id = models.PositiveIntegerField(
        'WordPress Image ID (where applicable)',
        null=True,
        blank=True,
    )
    
    width = models.IntegerField(
        'Image Width',
        default=820,
    )
    
    height = models.IntegerField(
        'Image Height',
        default=543,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link + ' -  ' + self.english
