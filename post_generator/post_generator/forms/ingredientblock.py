from nestedformset import NestedFormSet
from django.forms.models import inlineformset_factory
from post_generator.models import Post, Ingredient, IngredientBlock

class BaseIngredientBlockFormSet(NestedFormSet):
    def add_fields(self, form, index):
        # allow the super class to create the fields as usual
        super(BaseIngredientBlockFormSet, self).add_fields(form, index)

        # created the nested formset
        try:
            instance = self.get_queryset()[index]
        except IndexError:
            instance = None

        # store the formset in the .nested property
        form.nested = [
            IngredientFormSet(data = self.data if self.data and index is not None else None,
                            instance=instance,
                            prefix=form.prefix)]

IngredientFormSet = inlineformset_factory(IngredientBlock, Ingredient, extra=1)
IngredientBlockFormSet = inlineformset_factory(Post, IngredientBlock, formset=BaseIngredientBlockFormSet, extra=1)
