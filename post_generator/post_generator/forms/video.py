from post_generator.models import Post, Video
from django.forms.models import inlineformset_factory

VideoFormSet = inlineformset_factory(Post, Video, extra=1)
