from django.db import models
from post_generator.models.dictionaryitem import DictionaryItem
from post_generator.models.post import Post
from post_generator.models.header import Header

class Ingredient(models.Model):
    post = models.ForeignKey(Post)
    header = models.ForeignKey(Header)
    name = models.ForeignKey(DictionaryItem, related_name="name")
    size = models.ForeignKey(DictionaryItem, related_name="size", null=True, blank=True)
    quantity = models.CharField(max_length=20, null=True, blank=True)
    quant_units = models.ForeignKey(DictionaryItem, related_name="quant_units", null=True, blank=True)
    intl = models.CharField(max_length=20, null=True, blank=True)
    intl_units = models.ForeignKey(DictionaryItem, related_name="intl_units", null=True, blank=True)
    prep_style = models.ForeignKey(DictionaryItem, related_name="prep_style", null=True, blank=True)
    english_comment = models.CharField(max_length=250, null=True, blank=True)
    somali_comment = models.CharField(max_length=250, null=True, blank=True)
    french_comment = models.CharField(max_length=250, null=True, blank=True)
    arabic_comment = models.CharField(max_length=250, null=True, blank=True)
    optional = models.BooleanField()
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.name.english