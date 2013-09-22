from django.conf.urls import patterns, url

from post_generator import views

urlpatterns = patterns('',
    # ex: /post/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # ex: /post/new/
    url(r'^new/$', views.NewPost, name='new'),

    # ex: /post/5/
    url(r'^(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post'),
    
    # ex: /post/5/edit/
    url(r'^(?P<post_id>\d+)/edit/$', views.EditPost, name='edit'),

    # ex: /post/5/update/
    url(r'^(?P<post_id>\d+)/update/$', views.UpdatePost, name='update'),
)