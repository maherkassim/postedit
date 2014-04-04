from django.forms import ModelForm
from post_generator.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
