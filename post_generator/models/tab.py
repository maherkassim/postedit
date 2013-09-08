from django.db import models
from post_generator.models.language import Language
from post_generator.models.post import Post

class Tab(models.Model):
    post = models.ForeignKey(Post)
    
    language = models.ForeignKey(Language)
    
    include = models.BooleanField(
        'Include Tab in Post?',
    )
    
    class Meta:
        app_label = 'post_generator'
    
    def __unicode__(self):
        return self.post.title.english + ' - ' + self.language.full_name
