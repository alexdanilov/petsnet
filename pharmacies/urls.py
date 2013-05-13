from django.conf.urls import patterns, url

from pharmacies.views import PharmaciesList, PharmacyPage


urlpatterns = patterns('',
    url('^$', PharmaciesList.as_view(), name='pharmacies'),
    url('^(?P<pk>\d+)/$', PharmacyPage.as_view(), name='pharmacy'),
)
