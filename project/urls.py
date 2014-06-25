from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'c2s.views.home'),
)