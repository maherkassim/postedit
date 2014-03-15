from django.db import models

class DictionaryItem(models.Model):
    TYPE_CHOICES = (
        ('Noun', 'Noun'),
        ('Verb', 'Verb'),
        ('Adj.', 'Adjective'),
    )
    
    SET_CHOICES = (
         ('General', 'General'),
         ('Quant_Unit', 'Ingredient Quantity Unit'),
         ('Intl_Unit', 'Ingredient International Unit'),
         ('Size', 'Ingredient Size'),
         ('Prep_Type', 'Preparation/Type'),
    )
    
    _set = models.CharField('Set Type',
                            max_length=10,
                            choices=SET_CHOICES,
                            default='General',)
    
    word_type = models.CharField('Word Type',
                                 max_length=4,
                                 choices=TYPE_CHOICES,
                                 default='Noun',)

    english = models.CharField(
        'English',
        max_length=1000,
    )
    
    english_plural = models.CharField(
        'English - pluralized',
        max_length=1000,
        blank=True,
    )
    
    somali = models.CharField(
        'Somali',
        max_length=1000,
        blank=True,
    )
    
    french = models.CharField(
        'French masculine',
        max_length=1000,
        blank=True,
    )
    
    french_masculine_plural = models.CharField(
        'French - pluralized masculine',
        max_length=1000,
        blank=True,
    )
    
    french_feminine = models.CharField(
        'French - feminine',
        max_length=1000,
        blank=True,
    )
    
    french_feminine_plural = models.CharField(
        'French - pluralized feminine',
        max_length=1000,
        blank=True,
    )
    
    arabic = models.CharField(
        'Arabic',
        max_length=1000,
        blank=True,
    )
    
    image = models.URLField(
        'Image URL',
        blank=True,
    )
    
    link = models.URLField(
        'Recipe URL',
        blank=True,
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.english
