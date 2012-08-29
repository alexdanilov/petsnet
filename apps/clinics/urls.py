from django.conf.urls import patterns, url

from apps.clinics.views import ClinicsList, ClinicPage


urlpatterns = patterns('',
    url('^$', ClinicsList.as_view(), name='clinics'),
    url('^(?P<pk>\d+)/$', ClinicPage.as_view(), name='clinic'),
)
