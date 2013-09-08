from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from post_generator.models.post import Post

def index(request):
    latest_post_list = Post.objects.all()[:5]
    context = { 'latest_post_list': latest_post_list, }
    return render(request, 'post_generator/index.html', context)
    
def post(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_generator/detail.html', {'post': post_obj})