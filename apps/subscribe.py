#-*-coding: utf-8 -*-
from django.core.management import setup_environ
from django.core.mail import EmailMessage
from django.template import Context, Template
import settings

setup_environ(settings)


FROM_EMAIL = 'Anna Petsnet <content@petsnet.in.ua>'
SUBJECT = u'Обновите данные о Вашем питомнике в каталоге Petsnet'
file_data = open('../_files/nursery-anketa.doc').read()
html_template = open('templates/subscribes/nursery-update-info.html').read()

from apps.nurseries.models import Nursery
for item in Nursery.objects.filter(visibility=True):
    if not item.email:
        print 'Item %s skipped. Email is empty' % item.id
        continue

    html_content = Template(html_template).render(Context({'item': item}))

    msg = EmailMessage(SUBJECT, html_content, FROM_EMAIL, [item.email], headers={'Reply-To': 'content@petsnet.in.ua'})
    msg.content_subtype = "html"
    msg.attach('petsnet-anketa.doc', file_data, 'application/vnd.ms-word')
    
    msg.send()
    print 'Email for %s sent' % item.email
