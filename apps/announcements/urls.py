from django.conf.urls.defaults import patterns, url

from apps.announcements.views import *


urlpatterns = patterns('',
    url('^$', AnnouncementsList.as_view(), name='announcements'),
    
    url('^add/$', MyAnnouncementCreate.as_view(), name='my-announcements-add'),
    url('^my/$', MyAnnouncementsList.as_view(), name='my-announcements-list'),
    url('^edit/(?P<pk>\d+)/$', MyAnnouncementUpdate.as_view(), name='my-announcements-edit'),
    url('^delete/(?P<pk>\d+)/$', MyAnnouncementDelete.as_view(), name='my-announcements-delete'),
    
    url('^(?P<pk>\d+)/$', AnnouncementPage.as_view(), name='announcement'),
    url('^(?P<type>[\w\-]+)/$', AnnouncementsList.as_view(), name='announcements'),
)
