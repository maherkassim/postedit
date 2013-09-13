from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^post/', include('post_generator.urls', namespace="post_generator")),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^crossdomain\.xml$', TemplateView.as_view(template_name='crossdomain.xml')),
)
