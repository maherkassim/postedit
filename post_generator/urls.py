from django.conf.urls import patterns, url

from post_generator import views

urlpatterns = patterns('',
    # ex: /post/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # ex: /post/form/
    url(r'^form/$', views.ManagePost, name='post_new'),
    
    # ex: /post/form/5/
    url(r'^form/(?P<post_id>\d+)/$', views.ManagePost, name='post_manage'),

    # ex: /post/5    
    url(r'^(?P<post_id>\d+)/$', views.ViewPost, name='post_view'),
)
