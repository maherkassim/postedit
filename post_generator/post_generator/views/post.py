from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from post_generator.views import UpdateConversionIngredients
from post_generator.models import Post, Language, DictionaryItem
from post_generator.forms import PostForm, ImageFormSet, VideoFormSet, TextBlockFormSet, IngredientBlockFormSet, DirectionBlockFormSet

@login_required
def PostIndex(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'post_generator/post_index.html',
                              {'posts':posts,})

@login_required
def PostManage(request, post_id=False):
    post = Post()
    
    if post_id:
        post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        image_fs = ImageFormSet(request.POST, instance=post, prefix='images')
        video_fs = VideoFormSet(request.POST, instance=post, prefix='videos')
        text_block_fs = TextBlockFormSet(request.POST, instance=post, prefix='textblocks')
        ingredient_block_fs = IngredientBlockFormSet(request.POST, instance=post, prefix='ingredientblocks')
        direction_block_fs = DirectionBlockFormSet(request.POST, instance=post, prefix='directionblocks')
       
        # Check that Post object form is valid before saving and storing associated blocks
        if form.is_valid():
            form.save(commit=False)
            if image_fs.is_valid() and video_fs.is_valid() and text_block_fs.is_valid() and ingredient_block_fs.is_valid() and direction_block_fs.is_valid():
                form.save()
                image_fs.save()
                video_fs.save()
                text_block_fs.save()
                
                # When Ingredient objects are added to a Post, ensure that any new
                # or existing gram->cup conversion information is updated for each
                ingredient_block_fs.save_all()
                UpdateConversionIngredients(post.id)
                
                direction_block_fs.save_all()
                return redirect('post_generator:post_view', post_id=post.id)
    else:
        form = PostForm(instance=post)
        image_fs = ImageFormSet(instance=post, prefix='images')
        video_fs = VideoFormSet(instance=post, prefix='videos')
        text_block_fs = TextBlockFormSet(instance=post, prefix='textblocks')
        ingredient_block_fs = IngredientBlockFormSet(instance=post, prefix='ingredientblocks')
        direction_block_fs = DirectionBlockFormSet(instance=post, prefix='directionblocks')
    
    # Populate form lists (to be sent to template as part of the context)
    # - used to render various types of block forms in the interface
    blocks = []
    pretab_forms = []
    tabbed_forms = []
    template_forms = []
    deleted_forms = []
    for block_formset in image_fs, video_fs, text_block_fs, ingredient_block_fs, direction_block_fs:
        for block_form in block_formset.forms:
            if block_form['_loc_index'].value() < 0:
                # Filter for Template forms
                # - used to add new Block rows by addForm(Set) JS in the view
                block_form['DELETE'].field.initial = True
                block_form['_loc_index'].field.initial = 0
                template_forms.append(block_form)
            elif block_form['DELETE'].value():
                # Filter for Deleted forms
                # - used for Block rows that were deleted in the interface
                # - also used for Template forms on error (new set generated each time)
                deleted_forms.append(block_form)
            elif block_form['_tabbed'].value():
                # Filter for Tabbed forms
                # - used to display content in the English/Somali/... tabs
                tabbed_forms.append(block_form)
            else:
                # Filter for Pre-Tab Forms
                # - used to display content before language tabs
                pretab_forms.append(block_form)
    
    return render(request, 'post_generator/post_manage.html',
                              {'form':form,
                               'pretab_forms':sorted(pretab_forms, key=lambda form: form['_loc_index'].value()),
                               'tabbed_forms':sorted(tabbed_forms, key=lambda form: form['_loc_index'].value()),
                               'template_forms':template_forms,
                               'deleted_forms':deleted_forms,
                               'image_fs':image_fs,
                               'video_fs':video_fs,
                               'text_block_fs':text_block_fs,
                               'ingredient_block_fs':ingredient_block_fs,
                               'direction_block_fs':direction_block_fs,
                               'num_dict_items':DictionaryItem.objects.latest('id').id,
                               })

@login_required
def PostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_title = "%s (%s) %s %s" % (post.title.english,
                                    post.title.somali,
                                    post.title.french,
                                    post.title.arabic)
    
    # Sort blocks into defined array indices
    blocks = sorted(chain(post.image_set.all(), post.video_set.all(), post.textblock_set.all(), post.ingredientblock_set.all(), post.directionblock_set.all()),
                    key=attrgetter('_loc_index'))

    languages = [] 
    languages.append(Language.objects.get(name="english"))
    if post.include_somali:
        languages.append(Language.objects.get(name="somali"))
    if post.include_french:
        languages.append(Language.objects.get(name="french"))
    if post.include_arabic:
        languages.append(Language.objects.get(name="arabic"))
    # filter blocks 
    blocks_pretab = []
    blocks_tabbed = []
    for block in blocks:
        if block and block._tabbed:
            blocks_tabbed.append(block)
        elif block:
            blocks_pretab.append(block)
    
    headers = {}
    headers['directions'] = DictionaryItem.objects.get(english="Directions")
    headers['ingredients'] = DictionaryItem.objects.get(english="Ingredients")
    
    return render(request, 'post_generator/post_view.html',
                              {'post':post,
                               'post_title':post_title.title,
                               'blocks_pretab':blocks_pretab,
                               'blocks_tabbed':blocks_tabbed,
                               'languages':languages,
                               'headers':headers,
                              })

