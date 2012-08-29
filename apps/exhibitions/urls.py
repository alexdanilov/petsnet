from django.conf.urls import patterns, url

from apps.exhibitions.views import ExhibitionsList, ExhibitionPage


urlpatterns = patterns('',
    url('^$', ExhibitionsList.as_view(), name='exhibitions'),
    url('^(?P<pk>\d+)/$', ExhibitionPage.as_view(), name='exhibition'),
)
