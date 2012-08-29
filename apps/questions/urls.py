from django.conf.urls import patterns, url

from apps.questions.views import *


urlpatterns = patterns('',
    url('^$', QuestionsList.as_view(), name='questions'),
    
    url('^add/$', MyQuestionCreate.as_view(), name='my-question-add'),
    url('^my/$', MyQuestionsList.as_view(), name='my-questions-list'),
    url('^edit/(?P<pk>\d+)/$', MyQuestionUpdate.as_view(), name='my-question-edit'),
    url('^delete/(?P<pk>\d+)/$', MyQuestionDelete.as_view(), name='my-question-delete'),
    
    url('^(?P<pk>\d+)/$', QuestionPage.as_view(), name='question'),
)
