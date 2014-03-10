from django.shortcuts import render, redirect, get_object_or_404
from post_generator.models import Post, Language
from post_generator.forms import PostForm, ImageFormSet, VideoFormSet, TextBlockFormSet, IngredientBlockFormSet, DirectionBlockFormSet
from django.template import RequestContext

def ManagePost(request, post_id=False):
    post = Post()
    form = None
    image_fs = None
    video_fs = None
    text_block_fs = None
    ingredient_block_fs = None
    direction_block_fs = None
    if post_id:
       post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            image_fs = ImageFormSet(request.POST, instance=post)
            video_fs = VideoFormSet(request.POST, instance=post)
            text_block_fs = TextBlockFormSet(request.POST, instance=post)
            ingredient_block_fs = IngredientBlockFormSet(request.POST, instance=post)
            direction_block_fs = DirectionBlockFormSet(request.POST, instance=post)
            if image_fs.is_valid() and video_fs.is_valid() and text_block_fs.is_valid() and ingredient_block_fs.is_valid() and direction_block_fs.is_valid():
                form.save()
                image_fs.save()
                video_fs.save()
                text_block_fs.save()
                ingredient_block_fs.save_all()
                direction_block_fs.save_all()
                return redirect('post_generator:post_view', pk=post.id)
    
    else:
        form = PostForm(instance=post)
        image_fs = ImageFormSet(instance=post)
        video_fs = VideoFormSet(instance=post)
        text_block_fs = TextBlockFormSet(instance=post)
        ingredient_block_fs = IngredientBlockFormSet(instance=post)
        direction_block_fs = DirectionBlockFormSet(instance=post)
    
    return render(request, 'post_generator/post_form.html',
                              {'form':form,
                               'image_fs':image_fs,
                               'video_fs':video_fs,
                               'text_block_fs':text_block_fs,
                               'ingredient_block_fs':ingredient_block_fs,
                               'direction_block_fs':direction_block_fs,
                               })

def ViewPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_title = "%s (%s) %s %s" % (post.title.english,
                                    post.title.somali,
                                    post.title.french,
                                    post.title.arabic)
    block_count = post.image_set.count()
    block_count += post.video_set.count()
    block_count += post.textblock_set.count()
    block_count += post.ingredientblock_set.count()
    block_count += post.directionblock_set.count()
    blocks = [None] * (block_count);
    for query_set in (post.image_set.all(),
                      post.video_set.all(),
                      post.textblock_set.all(),
                      post.ingredientblock_set.all(),
                      post.directionblock_set.all()):
        for block in query_set:
            blocks[block._loc_index]=block

    return render(request, 'post_generator/post_view.html',
                              {'post':post,
                               'post_title':post_title.title,
                               'blocks':blocks,
                               'languages':Language.objects.all(),
                              })
