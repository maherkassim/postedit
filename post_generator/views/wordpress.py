import json, mimetypes

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from post_generator.models import Post
from user import U1, U2, U3
from django.views.decorators.csrf import csrf_exempt

def WPPostNew(request):
    client = Client(U1, U2, U3)
    new_post = WordPressPost()
    new_post.title = 'New Post'
    new_post.content = 'New Post'
    new_post.id = client.call(posts.NewPost(new_post))

    wp_post = client.call(posts.GetPost(new_post.id))
    data = json.dumps({'link':wp_post.link})
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def WPMediaUpload(request):
    client = Client(U1, U2, U3)
    if request.method == 'POST':
        upload_file = request.FILES['file']
        upload_name = upload_file.name
        upload_type = mimetypes.guess_type(upload_name)[0]
        upload_data = {
            'name':upload_name,
            'type':upload_type,
            'bits':xmlrpc_client.Binary(upload_file.read()),
        }
        response = client.call(media.UploadFile(upload_data))
        data = json.dumps(response)
        return HttpResponse(data, content_type='application/json')
