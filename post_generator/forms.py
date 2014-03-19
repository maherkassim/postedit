from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from post_generator.models import Language, DictionaryItem, Post, Image, Video, TextBlock, IngredientBlock, Ingredient, DirectionBlock, Direction
from django.forms.formsets import DELETION_FIELD_NAME

class PostForm(ModelForm):
    class Meta:
        model = Post

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

    def is_valid(self):
        result = super(RequiredInlineFormSet, self).is_valid()

        for form in self.forms:
            if hasattr(form, 'nested'):
                for n in form.nested:
                    # make sure each nested formset is valid as well
                    result = result and n.is_valid()
        return result
    
    def save_new(self, form, commit=True):
        """Saves and returns a new model instance for the given form."""
        
        instance = super(RequiredInlineFormSet, self).save_new(form, commit=commit)
        
        # update the form's instance reference
        form.instance = instance
        
        # update the instance reference on nested forms
        for nested in form.nested:
            nested.instance = instance
            
            # iterate over the cleaned_data of the nested formset and update the foreignkey reference
            for cd in nested.cleaned_data:
                cd[nested.fk.name] = instance
        
        return instance
    
    def should_delete(self, form):
        """Convenience method for determining if the form's object will
        be deleted; cribbed from BaseModelFormSet.save_existing_objects."""
        
        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
            return should_delete
        
        return False
    
    def save_all(self, commit=True):
        """Save all formsets and along with their nested formsets."""
        
        # Save without committing (so self.saved_forms is populated)
        # - We need self.saved_forms so we can go back and access
        #    the nested formsets
        objects = self.save(commit=False)
        
        # Save each instance if commit=True
        if commit:
            for o in objects:
                o.save()
        
        # save many to many fields if needed
        if not commit:
            self.save_m2m()
        
        # save the nested formsets
        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form): continue
            
            for nested in form.nested:
                nested.save(commit=commit)

class BaseIngredientBlockFormSet(RequiredInlineFormSet):
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
 
class BaseDirectionBlockFormSet(RequiredInlineFormSet):
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
    
ImageFormSet = inlineformset_factory(Post, Image, extra=1)
VideoFormSet = inlineformset_factory(Post, Video, extra=1)
TextBlockFormSet = inlineformset_factory(Post, TextBlock, extra=1)
IngredientBlockFormSet = inlineformset_factory(Post, IngredientBlock, formset=BaseIngredientBlockFormSet, extra=1)
DirectionBlockFormSet = inlineformset_factory(Post, DirectionBlock, formset=BaseDirectionBlockFormSet, extra=1)
IngredientFormSet = inlineformset_factory(IngredientBlock, Ingredient, extra=1)
DirectionFormSet = inlineformset_factory(DirectionBlock, Direction, extra=1)

