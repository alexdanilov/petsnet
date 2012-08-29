from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
    # account urls
    (r'^$', 'apps.users.account.signin'),
    (r'signin/$', 'apps.users.account.signin'),
    (r'signup/$', 'apps.users.account.signup'),
    (r'signout/$', 'apps.users.account.signout'),
    (r'loginza/$', 'apps.users.account.loginza'),

    # profile urls
    #(r'^(?P<user>\w+)/$', 'apps.users.profile.profile'),
    #(r'^(?P<user>\w+)/profile/$', 'apps.users.profile.profile'),
    #(r'^(?P<user>\w+)/animals/$', 'apps.users.profile.animals'),
    #(r'^(?P<user>\w+)/blog/$', 'apps.users.profile.blog_list'),
    #(r'^(?P<user>\w+)/blog/(?P<post>\d+)/$', 'apps.users.profile.blog_show'),
    #(r'^(?P<user>\w+)/friends/$', 'apps.users.profile.friends'),
    #(r'^(?P<user>\w+)/meetings/$', 'apps.users.profile.meetings'),
    #(r'^(?P<user>\w+)/photos/$', 'apps.users.profile.photos'),
)
