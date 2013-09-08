from django.conf.urls import patterns, url

from post_generator import views

urlpatterns = patterns('',
    # ex: /post_gen/
    url(r'^$', views.index, name='index'),

    # ex: /post_gen/post/5/
    url(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
)