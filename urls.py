from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.selection'),
    url(r'^historical/','blog.views.historical'),
    url(r'^dashboard/','blog.views.dashboard')
)
