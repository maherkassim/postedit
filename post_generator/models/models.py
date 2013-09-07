from django.db import models

# Assumptions:
#   - tab_index based ordering of items in post is consistent across all language tabs
#        - likely determined by array
#   - print options javascript always follows video insert
# To-do:
#   - add pluralization and gender to the dictionary
#   - release script should verify dictionary entries based on language (if included in post)

class Language(models.Model):
    full_name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.full_name

class DictionaryItem(models.Model):
    english = models.CharField(max_length=250)
    english_plural = models.CharField(max_length=250, null=True, blank=True)
    somali = models.CharField(max_length=250, null=True, blank=True)
    french = models.CharField(max_length=250, null=True, blank=True)
    french_plural = models.CharField(max_length=250, null=True, blank=True)
    arabic = models.CharField(max_length=250, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.english

class Post(models.Model):
    link = models.URLField()
    title = models.ForeignKey(DictionaryItem)

    def __unicode__(self):
        return self.title.english

class Tab(models.Model):
    post = models.ForeignKey(Post)
    language = models.ForeignKey(Language)
    include = models.BooleanField()

    def __unicode__(self):
        return self.post.title.english + ' - ' + self.language.full_name

class TextBlock(models.Model):
    post = models.ForeignKey(Post)
    post_intro = models.BooleanField()
    tab = models.ForeignKey(Tab)
    tab_index = models.PositiveIntegerField()
    text = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.text

class Header(models.Model):
    tab = models.ForeignKey(Tab)
    tab_index = models.PositiveIntegerField()
    text = models.ForeignKey(DictionaryItem)
    level = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return self.text.english

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

    def __unicode__(self):
        return self.name.english

class Direction(models.Model):
    post = models.ForeignKey(Post)
    tab_index = models.PositiveIntegerField()
    list_index = models.PositiveSmallIntegerField()
    english_text = models.CharField(max_length=250)
    somali_text = models.CharField(max_length=500, null=True, blank=True)
    french_text = models.CharField(max_length=500, null=True, blank=True)
    arabic_text = models.CharField(max_length=500, null=True, blank=True)
    
    def __unicode__(self):
        return self.english_text

class Image(models.Model):
    tab_index = models.PositiveIntegerField(null=True, blank=True)
    post = models.ForeignKey(Post)
    post_main = models.BooleanField()
    link = models.URLField()
    wordpress_image_id = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    english_caption = models.CharField(max_length=250, null=True, blank=True)
    somali_caption = models.CharField(max_length=250, null=True, blank=True)
    french_caption = models.CharField(max_length=250, null=True, blank=True)
    arabic_caption = models.CharField(max_length=250, null=True, blank=True)
    
    def __unicode__(self):
        return self.link

class Video(models.Model):
    tab_index = models.PositiveIntegerField()
    post = models.ForeignKey(Post)
    link = models.URLField()
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.link

