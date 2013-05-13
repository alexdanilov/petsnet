from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _



class Banner(models.Model):
    name = models.CharField(max_length=255, verbose_name = _('name'))
    code = models.SlugField(verbose_name = _('code'))
    content = models.TextField(verbose_name = _('content'))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'system_banners'
        verbose_name = _('banner')
        verbose_name_plural = _('banners')



class MailTemplate(models.Model):
    name = models.CharField(max_length=255, verbose_name = _('name'))
    slug = models.SlugField(verbose_name = _('slug'))
    subject = models.CharField(max_length=255, verbose_name = _('subject'))
    template = models.TextField(verbose_name = _('template'))

    def __unicode__(self):
        return self.name

    def send_mail(self, email, data):
        text = Template(self.template).render(Context(data))
        return send_mail(self.subject, text, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

    class Meta:
        db_table = 'system_mail_templates'
        verbose_name = _('mail_template')
        verbose_name_plural = _('mail_templates')



class Textblock(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('city'))
    slug = models.SlugField(max_length=255, verbose_name=_("slug"))
    body = models.TextField(verbose_name=_("body"))

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.visibility)

    class Meta:
        db_table = 'system_textblocks'
        verbose_name = _('textblock')
        verbose_name_plural = _('textblocks')



class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(max_length=255, verbose_name=_("slug"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    body = models.TextField(verbose_name=_("body"))
    page_title = models.CharField(blank=True, max_length=255, verbose_name=_("page_title"))
    page_description = models.CharField(blank=True, max_length=255, verbose_name=_("page_description"))
    page_keywords = models.TextField(blank=True, verbose_name=_("page_keywords"))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        db_table = 'system_pages'
        verbose_name = _("page")
        verbose_name_plural = _("pages")



class Setting(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("title"), editable=False)
    slug = models.SlugField(max_length=255, verbose_name=_("slug"), editable=False)
    value = models.CharField(max_length=255, verbose_name=_("value"))

    def __unicode__(self):
        return self.value

    class Meta:
        db_table = 'system_settings'
        verbose_name = _("settings")
        verbose_name_plural = _("settings")



class Region(models.Model):
    city = models.CharField(max_length=200)
    city_order = models.IntegerField()
    region_id = models.IntegerField()
    region = models.CharField(max_length=200)
    region_order = models.IntegerField()
    country_id = models.IntegerField()
    country = models.CharField(max_length=200)
    country_order = models.IntegerField()

    def __unicode__(self):
        return '%s, %s' % (self.city, self.region)

    class Meta:
        db_table = 'regions'
