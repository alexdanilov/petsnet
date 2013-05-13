from django.conf.urls import patterns, url

from nurseries.views import NurseriesList, NurseryPage


urlpatterns = patterns('',
    url('^$', NurseriesList.as_view(), name='nurseries'),
    url('^(?P<pk>\d+)/$', NurseryPage.as_view(), name='nursery'),
)
