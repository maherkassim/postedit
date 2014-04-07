import json

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from post_generator.models import Post
from user import U1, U2, U3

def WPPostNew(request):
    client = Client(U1, U2, U3)
    new_post = WordPressPost()
    new_post.title = 'New Post'
    new_post.content = 'New Post'
    new_post.id = client.call(posts.NewPost(new_post))

    wp_post = client.call(posts.GetPost(new_post.id))
    data = json.dumps({'link':wp_post.link})
    return HttpResponse(data, content_type='application/json')
