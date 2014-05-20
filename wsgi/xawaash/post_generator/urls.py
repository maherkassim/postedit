from django.conf.urls import patterns, url

from post_generator import views

urlpatterns = patterns('',
    url(r'^$', views.post_index, name='post_index'),
    url(r'^(?P<post_id>\d+)/$', views.post_view, name='post_view'),
    url(r'^form/$', views.post_manage, name='post_new'),
    url(r'^form/(?P<post_id>\d+)/$', views.post_manage, name='post_manage'),
    url(r'^dict/$', views.dictionary_item_index, name='dictionary_item_index'),
    url(r'^dict/(?P<pk>\d+)/$', views.dictionary_item_update.as_view(), name='dictionary_item_manage'),
    url(r'^dict/form/$', views.dictionary_item_create.as_view(), name='dictionary_item_new'),
    url(r'^dict/embed/(?P<pk>\d+)/$', views.dictionary_item_update_embed.as_view(), name='dictionary_item_manage_embed'),
    url(r'^dict/embed/form/$', views.dictionary_item_create_embed.as_view(), name='dictionary_item_new_embed'),
    url(r'^wp/new/$', views.wp_post_new, name='wp_new'),
    url(r'^wp/update/(?P<post_id>\d+)/$', views.wp_post_update, name='wp_update'),
    url(r'^wp/upload/$', views.wp_image_upload, name='wp_upload'),
    url(r'^ing/lookup/$', views.ingredient_intl_lookup, name='intl_lookup'),
)
