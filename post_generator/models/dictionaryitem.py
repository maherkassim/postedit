from django.db import models

class DictionaryItem(models.Model):
    english = models.CharField(
        'English Text',
        max_length=250,
    )

    english_plural = models.CharField(
        'Pluralized English Text',
        max_length=250,
        blank=True,
    )

    somali = models.CharField(
        'Somali Text',
        max_length=250,
        blank=True,
    )

    french = models.CharField(
        'French Text',
        max_length=250,
        blank=True,
    )
    
    french_plural = models.CharField(
        'Pluralized French Text',
        max_length=250,
        blank=True,
    )

    french_female = models.NullBooleanField(
        'French Gender (True:f, False:m)',
    )

    arabic = models.CharField(
        'Arabic Text',
        max_length=250,
        blank=True,
    )

    image = models.URLField(
        'Image URL',
        blank=True,
    )
    
    link = models.URLField(
        'Recipe URL',
        blank=True
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english
