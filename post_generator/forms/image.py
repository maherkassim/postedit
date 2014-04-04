from post_generator.models import Post, Image
from django.forms.models import inlineformset_factory

ImageFormSet = inlineformset_factory(Post, Image, extra=1)
