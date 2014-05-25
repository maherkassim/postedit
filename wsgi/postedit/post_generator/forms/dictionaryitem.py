from django.forms import ModelForm
from post_generator.models import DictionaryItem

class DictionaryItemForm(ModelForm):
    class Meta:
        model = DictionaryItem
