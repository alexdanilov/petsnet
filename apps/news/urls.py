from django.conf.urls import patterns, url

from apps.news.views import CatalogNewsList, CatalogNewsPage


urlpatterns = patterns('',
    url('^$', CatalogNewsList.as_view(), name='news-list'),
    url('^(?P<pk>\d+)/$', CatalogNewsPage.as_view(), name='news'),
)
