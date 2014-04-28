from datetime import time
from django.db import models
from post_generator.models import DictionaryItem

class Post(models.Model):
    link = models.URLField(
        'Xawaash Post URL',
    )
    
    pub_date = models.DateTimeField(
        'Date Published',
    )
    
    title = models.ForeignKey(DictionaryItem)
    
    featured_image = models.URLField(
        'Featured Image URL',
    )
    
    include_somali = models.BooleanField(
        'Include Somali tab in post?',
        default=True,
    )
    
    include_french = models.BooleanField(
        'Include French tab in post?',
        default=False,
    )
    
    include_arabic = models.BooleanField(
        'Include Arabic tab in post?',
        default=True,
    )
    
    servings = models.IntegerField(
        'Number of servings',
    )
    
    prep_time = models.TimeField(
        'Preparation Time',
        default=time(0,0),
    )

    cook_time = models.TimeField(
        'Cooking Time',
        default=time(0,0),
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.title.english
