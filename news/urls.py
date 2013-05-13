from django.conf.urls import patterns, url

from news.views import NewsList, NewsPage


urlpatterns = patterns('',
    url('^$', NewsList.as_view(), name='news_list'),
    url('^(?P<pk>\d+)/$', NewsPage.as_view(), name='news_show'),
)
