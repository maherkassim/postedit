from django.conf.urls import patterns, url

from post_generator import views

urlpatterns = patterns('',
    # ex: /post/
    url(r'^$', views.PostIndex, name='post_index'),

    # ex: /post/form/
    url(r'^form/$', views.PostManage, name='post_new'),
    
    # ex: /post/form/5/
    url(r'^form/(?P<post_id>\d+)/$', views.PostManage, name='post_manage'),

    # ex: /post/5    
    url(r'^(?P<post_id>\d+)/$', views.PostView, name='post_view'),
)
