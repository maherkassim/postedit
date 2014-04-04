from post_generator.models import Post, TextBlock
from django.forms.models import inlineformset_factory

TextBlockFormSet = inlineformset_factory(Post, TextBlock, extra=1)
