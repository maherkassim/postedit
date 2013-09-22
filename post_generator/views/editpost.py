# -*- coding: utf-8 -*-
import re

from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from post_generator.models.tab import Tab
from post_generator.models.post import Post
from post_generator.models.image import Image
from post_generator.models.video import Video
from post_generator.models.header import Header
from post_generator.models.language import Language
from post_generator.models.direction import Direction
from post_generator.models.textblock import TextBlock
from post_generator.models.ingredient import Ingredient
from post_generator.models.dictionaryitem import DictionaryItem

# Defaults for first two items of DictionaryItem database
PRINT_ID = 1
PRINT_IMG_ID = 2

def create_print_objs():
    print_defaults = {
        'english':"Print Recipe",
        'somali':"Daabac Soo'da",
        'french':"Imprimer la Recette",
        'arabic':"اطبع الوصفة - بدون صور"
    }
    
    print_img_defaults = {
        'english':"Print Recipe with Photos",
        'somali':"Daabac Soo'da oo Sawirro Leh",
        'french':"Imprimer la Recette avec Photos",
        'arabic':"اطبع الوصفة - مع صور"
    }
    DictionaryItem.objects.create(id=PRINT_ID, **print_defaults)
    DictionaryItem.objects.create(id=PRINT_IMG_ID, **print_img_defaults)

def get_print_obj(print_id):
    try:
        print_obj = DictionaryItem.objects.get(id=print_id)
    except DictionaryItem.DoesNotExist:
        create_print_objs()
        print_obj = DictionaryItem.objects.get(id=print_id)
    return print_obj

def NewPost(request):
    languages = Language.objects.all()
    lang_list = []
    for lang in languages:
        lang_list.append(lang.full_name)
    
    # Retrieve objects containing translations for print options.
    # Used to set default values in text input fields
    #   (see new.html template).
    print_obj = get_print_obj(PRINT_ID)
    print_img_obj = get_print_obj(PRINT_IMG_ID)
    
    print_dict = {}
    for lang in lang_list:
        print_dict[lang] = print_obj.__dict__[lang]
    
    print_img_dict = {}
    for lang in lang_list:
        print_img_dict[lang] = print_img_obj.__dict__[lang]
    
    # Create new Post object initialized with placeholder title
    temp_title = "New Post " + timezone.now().strftime("%s %s" % ("%Y-%m-%d",
                                                                  "%H:%M:%S"))
    title_obj = DictionaryItem.objects.create(english = temp_title)
    post_obj = Post(
        link="http://xawaash.com/?p=",
        title=title_obj,
        pub_date=timezone.now()
    )
    post_obj.save()
    
    context = {
        'post':post_obj,
        'lang_list':lang_list,
        'print_def':print_dict,
        'tab_sides':['left', 'right'],
        'print_img_def':print_img_dict,
	}
    return render(request, 'post_generator/new.html', context)

def EditPost(request, post_id):
	context = {
		'post':'post',
		'lang_list':'lang_list',
		'print_def':'print_dict',
		'tab_sides':['left', 'right'],
		'print_img_def':'print_img_dict',
	}
	return render(request, 'post_generator/edit.html', context)

def sub_dict(dictionary, regex):
    # Gives sub-dictionary where all keys contain string
    return dict((key, value)
        for key,value in dictionary.iteritems() if regex.search(key))

def update_dictionaryitem(request, lang_obj_list, field_name, item_id=0):
    query_args = Q()
    update_args = {}
    for lang_obj in lang_obj_list:
        item_field = lang_obj.full_name + field_name
        item_text = request.POST[item_field]
        query_args = query_args | Q(**{lang_obj.full_name: item_text})
        update_args[lang_obj.full_name] = item_text
    try:
        if item_id:
            item_obj = DictionaryItem.objects.get(id=item_id)
        else:
            item_obj = DictionaryItem.objects.filter(query_args)[:1].get()
    except DictionaryItem.DoesNotExist:
        item_obj = DictionaryItem(**update_args)
    else:
        item_obj = DictionaryItem(id=item_obj.id, **update_args)
    
    item_obj.save()
    return item_obj

def update_post_title(request, post_obj, lang_obj_list):
    # Update Post object with new link and title
    
    title_obj = update_dictionaryitem(request, lang_obj_list, '-title')
    post_url = request.POST['post-url']
    title_obj.link = post_url
    title_obj.save()
    
    post_obj.link = post_url
    post_obj.title = title_obj
    post_obj.save()

def update_post_tabs(request, post_obj, lang_obj_list):
    # Create Tab objects
    
    lang_dict = {}
    # lang_dict: Dictionary with Language names as keys and values
    #   indicating whether that language should be rendered.
    #   This is used to determine whether or not to completely skip
    #   processing the data in a particular languauge's tab.
    
    for lang_obj in lang_obj_list:
        # Get boolean of whether tab should be included from POST
        include_str = lang_obj.full_name + '-include'
        include_tab = request.POST.get(include_str, False)
        
        # Update lang_dict with new status for inclusion of language
        lang_dict[lang_obj.full_name] = include_tab
        
        try:
            tab_obj = post_obj.tab_set.get(language=lang_obj)
        except Tab.DoesNotExist:
            post_obj.tab_set.create(
                language=lang_obj,
                include=include_tab
            )
        else:
            tab_obj.include = include_tab
            tab_obj.save()
    return lang_dict

def update_post_print_opts(request, lang_obj_list):
    update_dictionaryitem(request, lang_obj_list, '-print', PRINT_ID)
    update_dictionaryitem(request, lang_obj_list, '-print-img', PRINT_IMG_ID)

def update_post_textblocks(request, post_obj, lang_obj, text_type, base_ind):
    tab_obj = post_obj.tab_set.get(language=lang_obj)
    
    # Create regex and filter for TextBlock data in request.POST
    regex_base_pattern = lang_obj.full_name + '-' + text_type + '-'
    regex = re.compile('^' + regex_base_pattern + '(?P<item_ind>\d+)$')
    item_dict = sub_dict(request.POST, regex)
    
    block_count = 0
    for block in block_dict.keys():
        # Determine position of text block in tab (tab_index)
        match = regex.search(block)
        block_ind = match.group('block_ind')
        tab_ind = block_ind + base_ind
        block_count += 1
        
        # Retrieve actual block text 
        block_text = block_dict[key]
        
        # Determine if textblock should be included for printing option
        print_field = regex_base_pattern + 'print-' + block_ind
        block_print = request.POST.get(print_field, False)
        
        # Update existing TextBlock or create new
        try:
            block_obj = post_obj.textblock_set.get(tab=tab_obj,
                                                   tab_index=tab_ind)
        except TextBlock.DoesNotExist:
            post_obj.textblock_set.create(
                tab=tab_obj,
                text=block_text,
                tab_index=tab_ind,
                printable=block_print
                post_intro=(text_type == intro),
            )
        else:
            block_obj.text = block_text
            block_obj.printable = block_print
    return base_ind + block_count

def UpdatePost(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    
    lang_obj_list = Language.objects.all()
    update_post_title(request, post_obj, lang_obj_list)
    lang_dict = update_post_tabs(request, post_obj, lang_obj_list)
    update_post_print_opts(request, lang_obj_list)
    
    base_tab_ind = 0
    
    for lang_obj in lang_obj_list:
        if not lang_dict[lang_obj.full_name]:
            continue
        base_tab_ind = update_post_textblocks(
                        request, post_obj, lang_obj, 'intro', base_tab_ind)
    
    return HttpResponseRedirect(reverse('post_generator:post',
                                        args=(post_obj.id,)))


















