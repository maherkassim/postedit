from django.shortcuts import render, redirect, get_object_or_404
from post_generator.models import DictionaryItem
from post_generator.forms import DictionaryItemForm

def DictionaryItemIndex(request):
    dictionary_items = DictionaryItem.objects.all()
    return render(request, 'post_generator/dictionary_item_index.html',
                           {'dictionary_items':dictionary_items,})

def DictionaryItemManage(request, item_id=False):
    dictionary_item = DictionaryItem()
    if item_id:
        dictionary_item = get_object_or_404(DictionaryItem, id=item_id)
    if request.method == 'POST':
        form = DictionaryItemForm(request.POST, instance=dictionary_item)
        if form.is_valid():
            form.save()
            return redirect('post_generator:dictionary_item_index')
    else:
        form = DictionaryItemForm(instance=dictionary_item)
    return render(request, 'post_generator/dictionary_item_manage.html',
                               {'form':form,})

