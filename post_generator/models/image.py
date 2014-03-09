from django.db import models
from post_generator.models import Post, DictionaryItem

class Image(models.Model):
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=-1,
    )
    
    post = models.ForeignKey(Post)
    
    caption = models.ForeignKey(
        DictionaryItem,
        related_name="image_caption",
        verbose_name="Image Caption",
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
        default=820,
    )
    
    height = models.PositiveSmallIntegerField(
        'Image Height',
        default=543,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.link
