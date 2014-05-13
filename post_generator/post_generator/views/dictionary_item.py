import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404

from post_generator.models import DictionaryItem
from post_generator.forms import DictionaryItemForm

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response

class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class DictionaryItemCreateEmbed(AjaxableResponseMixin, LoginRequiredMixin, CreateView):
    model = DictionaryItem
    form_class = DictionaryItemForm
    template_name = 'post_generator/dictionary_item_manage_embed.html'
    success_url = reverse_lazy('post_generator:dictionary_item_index')

class DictionaryItemUpdateEmbed(AjaxableResponseMixin, LoginRequiredMixin, UpdateView):
    model = DictionaryItem
    form_class = DictionaryItemForm
    template_name = 'post_generator/dictionary_item_manage_embed.html'
    success_url = reverse_lazy('post_generator:dictionary_item_index')

class DictionaryItemCreate(AjaxableResponseMixin, LoginRequiredMixin, CreateView):
    model = DictionaryItem
    form_class = DictionaryItemForm
    template_name = 'post_generator/dictionary_item_manage.html'
    success_url = reverse_lazy('post_generator:dictionary_item_index')

class DictionaryItemUpdate(AjaxableResponseMixin, LoginRequiredMixin, UpdateView):
    model = DictionaryItem
    form_class = DictionaryItemForm
    template_name = 'post_generator/dictionary_item_manage.html'
    success_url = reverse_lazy('post_generator:dictionary_item_index')

@login_required
def DictionaryItemIndex(request):
    dictionary_items = DictionaryItem.objects.all()
    return render(request, 'post_generator/dictionary_item_index.html',
                           {'dictionary_items':dictionary_items,})
