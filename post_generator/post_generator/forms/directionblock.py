from nestedformset import NestedFormSet
from django.forms.models import inlineformset_factory
from post_generator.models import Post, Direction, DirectionBlock

class BaseDirectionBlockFormSet(NestedFormSet):
    def add_fields(self, form, index):
        # allow the super class to create the fields as usual
        super(BaseDirectionBlockFormSet, self).add_fields(form, index)

        # created the nested formset
        try:
            instance = self.get_queryset()[index]
        except IndexError:
            instance = None

        # store the formset in the .nested property
        form.nested = [
            DirectionFormSet(data = self.data if self.data and index is not None else None,
                            instance=instance,
                            prefix=form.prefix)]

DirectionFormSet = inlineformset_factory(DirectionBlock, Direction, extra=1)
DirectionBlockFormSet = inlineformset_factory(Post, DirectionBlock, formset=BaseDirectionBlockFormSet, extra=1)
