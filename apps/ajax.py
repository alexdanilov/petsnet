from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^get-breeds/$', 'apps.animals.views.ajax_get_breeds'),
    url(r'^get-cities/$', 'apps.system.views.ajax_get_cities'),
    url(r'^get-users/$', 'apps.users.views.ajax_get_users'),

    url(r'^friend-add/(?P<friend>\d+)/$', 'apps.users.my.ajax_friend_add'),
    url(r'^friend-delete/$', 'apps.users.my.ajax_friend_delete'),
)
