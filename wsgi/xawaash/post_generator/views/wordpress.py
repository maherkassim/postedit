import os
import re
import json
import Image
import mimetypes
import cStringIO

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from post_generator.models import Post

@login_required
def WPPostNew(request):
    client = Client(os.environ['POSTGEN_WP_TARGET'], os.environ['POSTGEN_WP_USER'], os.environ['POSTGEN_WP_PASS'])
    new_post = WordPressPost()
    new_post.title = 'New Post'
    new_post.content = 'New Post'
    new_post.id = client.call(posts.NewPost(new_post))

    wp_post = client.call(posts.GetPost(new_post.id))
    data = json.dumps({'link':wp_post.link})
    return HttpResponse(data, content_type='application/json')

def get_french(dict_item):
    return dict_item.french or dict_item.french_feminine

@login_required
@csrf_exempt
def WPPostUpdate(request, post_id):
    if request.method == 'POST':
        client = Client(os.environ['POSTGEN_WP_TARGET'], os.environ['POSTGEN_WP_USER'], os.environ['POSTGEN_WP_PASS'])
        post_obj = Post.objects.get(pk=post_id)
        post_title = post_obj.title.english
        if post_obj.title.somali:
            post_title += ' (' + post_obj.title.somali + ')'
        french_title = get_french(post_obj.title)
        if french_title:
            post_title += ' ' + french_title
        if post_obj.title.arabic:
            post_title += ' ' + post_obj.title.arabic
        post_title += ' - Post Generator'
        
        matches = re.search('.*=(\d+)$', post_obj.link)
        wp_post_id = matches.group(1)
        current_post = client.call(posts.GetPost(wp_post_id))
        wp_post = WordPressPost()
        wp_post.title = post_title
        wp_post.content = request.POST['post-content']
        wp_post.date = post_obj.pub_date
        if current_post.thumbnail['attachment_id'] != str(post_obj.featured_image_id):
            wp_post.thumbnail = str(post_obj.featured_image_id)

        client.call(posts.EditPost(wp_post_id, wp_post))
        data = json.dumps({'status':True})
        return HttpResponse(data, content_type='application/json')

@login_required
@csrf_exempt
def WPMediaUpload(request):
    if request.method == 'POST':
        client = Client(os.environ['POSTGEN_WP_TARGET'], os.environ['POSTGEN_WP_USER'], os.environ['POSTGEN_WP_PASS'])
        upload_file = request.FILES['file']
        file_buf = upload_file.read()
        upload_name = upload_file.name
        upload_type = mimetypes.guess_type(upload_name)[0]
        upload_data = {
            'name':upload_name,
            'type':upload_type,
            'bits':xmlrpc_client.Binary(file_buf),
        }
        response = client.call(media.UploadFile(upload_data))
        img = Image.open(cStringIO.StringIO(file_buf))
        width, height = img.size
        response_data = {
            'id':response['id'],
            'link':response['url'],
            'width':width,
            'height':height,
        }
        data = json.dumps(response_data)
        return HttpResponse(data, content_type='application/json')
