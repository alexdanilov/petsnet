from django.conf.urls import patterns, url

from apps.news.views import NewsList, NewsPage


urlpatterns = patterns('',
    url('^$', NewsList.as_view(), name='news-list'),
    url('^(?P<pk>\d+)/$', NewsPage.as_view(), name='news'),
)
