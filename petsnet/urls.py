from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from autocomplete.views import autocomplete
from petsnet.views import IndexView, PageView, LogsList
from content.views import ArticlesList, ArticlePage


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),

    # System urls
    (r'^account/', include('users.urls')),
    (r'^users/', include('users.urls')),
    (r'^ajax/', include('petsnet.ajax')),
    (r'^cpanel/', include(admin.site.urls)),
    url('^content-logs/', LogsList.as_view(), name='logs'),
    
    # Catalog content
    (r'^clinics/', include('clinics.urls')),
    (r'^exhibitions/', include('exhibitions.urls')),
    (r'^nurseries/', include('nurseries.urls')),
    (r'^news/', include('news.urls')),
    (r'^pharmacies/', include('pharmacies.urls')),

    # Other urls
    url('^articles/(?P<pk>\d+)/', ArticlePage.as_view(), name='article'),
    url('^articles/(?P<category>\w+)/', ArticlesList.as_view(), name='articles'),
    url('^articles/', ArticlesList.as_view(), name='articles'),
    url('^page/(?P<slug>\w+)/$', PageView.as_view(), name='page'),

    # User content
    (r'^announcements/', include('announcements.urls')),
    (r'^blogs/', 'blogs.views.list'),
    (r'^questions/', include('questions.urls')),
    (r'^page/(?P<slug>\d+)$', 'content.views.page'),

    # Django extensions
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^autocomplete/', include(autocomplete.urls)),
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
