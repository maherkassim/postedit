from django.db import models
from post_generator.models import Post

class TextBlock(models.Model):
    post = models.ForeignKey(Post)
    
    _loc_index = models.PositiveIntegerField(
        'Relative location on page',
        default=-1,
    )
    
    _tabbed = models.BooleanField(
        default=True,
    )
    
    english = models.TextField(
        'English Text/Paragraph',
    )
    
    french = models.TextField(
        'French Text/Paragraph',
        blank=True,
    )
    
    french_author = models.CharField(
        'French Author',
        max_length=1000,
        blank=True,
    )
    
    somali = models.TextField(
        'Somali Text/Paragraph',
        blank=True,
    )
    
    somali_author = models.CharField(
        'Somali Author',
        max_length=1000,
        blank=True,
    )
    
    arabic = models.TextField(
        'Arabic Text/Paragraph',
        blank=True,
    )

    arabic_author = models.CharField(
        'Arabic Author',
        max_length=1000,
        blank=True,
    )
    
    printable = models.BooleanField(
        'Make this text block printable?',
    )
    
    header = models.BooleanField(
        'Is this text a header?',
        default = False,
    )
    
    inline_styles = models.CharField(
        'Custom Styles',
        max_length=1000,
        default="",
        blank=True,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return unicode(self.english)
