from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils import timezone

from post_generator.models.post import Post

class IndexView(ListView):
    template_name = 'post_generator/index.html'
    context_object_name = 'latest_post_list'
    
    def get_queryset(self):
        """
        Return the last five published posts (not including those set to be
        published in the future).
        """
        return Post.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_generator/detail.html'
