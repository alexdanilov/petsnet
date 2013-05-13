from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from autocomplete.views import autocomplete
from apps.views import IndexView, PageView, LogsList
from apps.content.views import ArticlesList, ArticlePage


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),

    # System urls
    (r'^account/', include('apps.users.urls')),
    (r'^users/', include('apps.users.urls')),
    (r'^ajax/', include('apps.ajax')),
    (r'^cpanel/', include(admin.site.urls)),
    url('^content-logs/', LogsList.as_view(), name='logs'),
    
    # Catalog content
    (r'^clinics/', include('apps.clinics.urls')),
    (r'^exhibitions/', include('apps.exhibitions.urls')),
    (r'^nurseries/', include('apps.nurseries.urls')),
    (r'^news/', include('apps.news.urls')),
    (r'^pharmacies/', include('apps.pharmacies.urls')),

    # Other urls
    url('^articles/(?P<pk>\d+)/', ArticlePage.as_view(), name='article'),
    url('^articles/(?P<category>\w+)/', ArticlesList.as_view(), name='articles'),
    url('^articles/', ArticlesList.as_view(), name='articles'),
    url('^page/(?P<slug>\w+)/$', PageView.as_view(), name='page'),

    # User content
    (r'^announcements/', include('apps.announcements.urls')),
    (r'^blogs/', 'apps.blogs.views.list'),
    (r'^questions/', include('apps.questions.urls')),
    (r'^page/(?P<slug>\d+)$', 'apps.content.views.page'),

    # Django extensions
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^autocomplete/', include(autocomplete.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    #url(r'^ulogin/', include('django_ulogin.urls')),
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
