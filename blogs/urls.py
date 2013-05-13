from django.conf.urls.defaults import patterns


urlpatterns = patterns('apps.blogs.views',
    (r'^edit/(?P<id>\d+)/$', 'edit'),
    (r'^delete/(?P<id>\d+)/$', 'delete'),
    (r'^add/$', 'edit'),
    (r'^$', 'my'),
)
