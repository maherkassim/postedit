from django.conf.urls import patterns, url

from post_generator import views

urlpatterns = patterns('',
    # ex: /post/
    url(r'^$', views.PostIndex, name='post_index'),

    # ex: /post/5    
    url(r'^(?P<post_id>\d+)/$', views.PostView, name='post_view'),

    # ex: /post/form/
    url(r'^form/$', views.PostManage, name='post_new'),
    
    # ex: /post/form/5/
    url(r'^form/(?P<post_id>\d+)/$', views.PostManage, name='post_manage'),
    
    # ex: post/dict/
    url(r'^dict/$', views.DictionaryItemIndex, name='dictionary_item_index'),
     
    # ex: post/dict/5/
    url(r'^dict/(?P<item_id>\d+)/$', views.DictionaryItemManage, name='dictionary_item_manage'),
    
    # ex: post/dict/form/
    url(r'^dict/form/$', views.DictionaryItemManage, name='dictionary_item_new'),
)
