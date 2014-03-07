from django.shortcuts import render, redirect, get_object_or_404
from post_generator.models import Post
from post_generator.forms import PostForm, ImageFormSet, VideoFormSet, TextBlockFormSet, IngredientBlockFormSet, DirectionBlockFormSet
from django.template import RequestContext

def ManagePosts(request, post_id=False):
    if post_id:
       post = get_object_or_404(Post, id=post_id)
    else:
       post=Post()
    form = None
    image_fs = None
    video_fs = None
    text_block_fs = None
    ingredient_block_fs = None
    direction_block_fs = None
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
                return redirect('post_generator:post', pk=post.id)
    
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

