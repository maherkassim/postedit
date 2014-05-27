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
def wp_post_new(request):
    """
    Create a New Post and returns the link via WordPress XML-RPC API.
    
    Populates with temporary information (updated later by :view:`post_generator.views.wordpress.wp_post_update`)
    """
    client = Client(os.environ['POSTGEN_WP_TARGET'], os.environ['POSTGEN_WP_USER'], os.environ['POSTGEN_WP_PASS'])
    
    # Create WP post object and populate with placeholder information
    # - Updated later by WPPostUpdate (post_generator:wp_update)
    new_post = WordPressPost()
    new_post.title = 'New Post'
    new_post.content = 'New Post'
    new_post.id = client.call(posts.NewPost(new_post))
    
    wp_post = client.call(posts.GetPost(new_post.id))
    data = json.dumps({'link':wp_post.link})
    return HttpResponse(data, content_type='application/json')

@login_required
@csrf_exempt
def wp_post_update(request, post_id):
    """
    Update WordPress post using Post object and HTML
    
    Primarily for 'Update This Post' button AJAX function in :view:`post_generator.views.post.post_view`
    
    :param post_id: :model:`post_generator.Post` to update WP post with
    :type post_id: :model:`post_generator.Post`
    """
    
    # TODO: add case for GET request
    if request.method == 'POST':
        client = Client(os.environ['POSTGEN_WP_TARGET'], os.environ['POSTGEN_WP_USER'], os.environ['POSTGEN_WP_PASS'])
        post_obj = Post.objects.get(pk=post_id)
        
        # Generate Multilingual title
        post_title = post_obj.title.english
        if post_obj.title.somali:
            post_title += ' (' + post_obj.title.somali + ')'
        if post_obj.title.french or post_obj.title.french_feminine:
            post_title += ' ' + (post_obj.title.french or post_obj.title.french_feminine)
        if post_obj.title.arabic:
            post_title += ' ' + post_obj.title.arabic
        post_title += ' - PostGen'
        
        # Pull WP post ID from stored link
        matches = re.search('.*=(\d+)$', post_obj.link)
        wp_post_id = matches.group(1)
        
        # Create new WP post object with data
        wp_post = WordPressPost()
        wp_post.title = post_title
        wp_post.content = request.POST['post-content']
        wp_post.date = post_obj.pub_date
        
        # Retrieve current post data via WP XML-RPC API
        # - Used to determine whether featured_image_id data should be included
        #   - Avoids error from setting featured_image_id to the one already attached
        current_post = client.call(posts.GetPost(wp_post_id))
        if not current_post.thumbnail or current_post.thumbnail['attachment_id'] != str(post_obj.featured_image_id):
            wp_post.thumbnail = str(post_obj.featured_image_id)
        
        # Update WP post and return status=True via JSON
        client.call(posts.EditPost(wp_post_id, wp_post))
        return HttpResponse(json.dumps({'status':True}), content_type='application/json')

@login_required
@csrf_exempt
def wp_image_upload(request):
    """
    Used to upload media (primarily images) to WordPress
    
    Primarily for :model:`post_generator.Image` AJAX upload form in :view:`post_generator.views.post.post_manage`
    """
    
    # TODO: add case for GET request
    if request.method == 'POST':
        client = Client(os.environ['POSTGEN_WP_TARGET'], os.environ['POSTGEN_WP_USER'], os.environ['POSTGEN_WP_PASS'])
        
        # Read submitted file data into a buffer
        upload_file = request.FILES['file']
        file_buf = upload_file.read()
        
        # Upload file data to WP via XML-RPC API
        upload_name = upload_file.name
        upload_type = mimetypes.guess_type(upload_name)[0]
        upload_data = {
            'name':upload_name,
            'type':upload_type,
            'bits':xmlrpc_client.Binary(file_buf),
        }
        response = client.call(media.UploadFile(upload_data))
        
        # Determine image width and height
        img = Image.open(cStringIO.StringIO(file_buf))
        width, height = img.size
        
        # Combine and return Image data via JSON
        response_data = {
            'id':response['id'],
            'link':response['url'],
            'width':width,
            'height':height,
        }
        data = json.dumps(response_data)
        return HttpResponse(data, content_type='application/json')

