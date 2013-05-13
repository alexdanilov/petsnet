from django.conf.urls import patterns, url

from questions.views import *


urlpatterns = patterns('',
    url('^$', QuestionsList.as_view(), name='questions'),
    
    url('^add/$', MyQuestionCreate.as_view(), name='question_add'),
    url('^my/$', MyQuestionsList.as_view(), name='questions_my'),
    url('^edit/(?P<pk>\d+)/$', MyQuestionUpdate.as_view(), name='question_edit'),
    url('^delete/(?P<pk>\d+)/$', MyQuestionDelete.as_view(), name='question_delete'),
    
    url('^(?P<pk>\d+)/$', QuestionPage.as_view(), name='question'),
)
