from django.conf import settings
from django.conf.urls import patterns, include
from django.contrib import admin
from autocomplete.views import autocomplete

from apps.views import IndexView


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', IndexView.as_view()),

    # System urls
    (r'^account/', include('apps.users.urls')),
    (r'^users/', include('apps.users.urls')),
    (r'^ajax/', include('apps.ajax')),
    (r'^cpanel/', include(admin.site.urls)),
    
    # Catalog content
    (r'^clinics/', include('apps.clinics.urls')),
    (r'^exhibitions/', include('apps.exhibitions.urls')),
    (r'^nurseries/', include('apps.nurseries.urls')),
    (r'^news/', include('apps.news.urls')),
    (r'^pharmacies/', include('apps.pharmacies.urls')),

    # User content
    (r'^announcements/', include('apps.announcements.urls')),
    (r'^blogs/', 'apps.blogs.views.list'),
    (r'^questions/', include('apps.questions.urls')),
    (r'^page/(?P<slug>\d+)$', 'apps.content.views.page'),

    # Django extensions
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^autocomplete/', include(autocomplete.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^autocomplete/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + 'autocomplete/',
        }),
        (r'^i/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + 'i/',
        }),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + 'js/',
        }),
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + 'css/',
        }),
        (r'^u/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + 'u/',
        }),
        (r'^admin_tools/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + 'admin_tools/',
        }),
   )
