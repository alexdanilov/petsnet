#-*-coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

from tinymce import models as tinymce_models
from apps.system.models import Region


class ClinicService(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'clinic_services'
        verbose_name = _("clinic-service")
        verbose_name_plural = _("clinic-services")


CALL_STATUSES = (
    ('call', u'Позвонить'),
    ('recall', u'Перезвонить'),
    ('called', u'Уже позвонили'),
)
class Clinic(models.Model):
    region = models.ForeignKey(Region, verbose_name=_("region"), db_index=True)

    name = models.CharField(max_length=255, verbose_name=_("name"))
    about = tinymce_models.HTMLField(verbose_name=_("description"), blank=True)
    address = models.CharField(max_length=255, verbose_name=_("address"))
    phones = models.CharField(max_length=255, verbose_name=_("phones"), blank=True)
    website = models.URLField(max_length=255, verbose_name=_("website"), blank=True)
    email = models.EmailField(max_length=255, verbose_name=_("email"), blank=True)

    working_hours = models.CharField(max_length=64, verbose_name=_("working_hours"), blank=True)
    working_hours_saturday = models.CharField(max_length=64, verbose_name=_("working_hours_saturday"), blank=True, null=True)
    working_hours_sanday = models.CharField(max_length=64, verbose_name=_("working_hours_sanday"), blank=True, null=True)

    services = models.ManyToManyField(ClinicService, verbose_name=_("clinic-services"), blank=True)
    prices = tinymce_models.HTMLField(verbose_name=_("prices"), blank=True)
    coworkers = tinymce_models.HTMLField(verbose_name=_("coworkers"), blank=True)

    last_call_date = models.DateTimeField(verbose_name=_("last_call_date"), blank=True)
    call_status = models.CharField(max_length=10, verbose_name=_('call_status'), choices=CALL_STATUSES)

    order_num = models.IntegerField(verbose_name=_("order_num"), blank=True)
    visibility = models.BooleanField(default=True, verbose_name=_("visibility"), db_index=True)

    @property
    def phones_list(self):
        return self.phones.split(',')

    @property
    def url(self):
        return '/clinics/%s' % self.id

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order_num']
        db_table = 'clinics'
        verbose_name = _("clinic")
        verbose_name_plural = _("clinics")


# Admin classes
class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city',)


class ClinicServiceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(ClinicService, ClinicServiceAdmin)


class ClinicAdmin(AutocompleteAdmin, admin.ModelAdmin):
    list_display = ['name', 'region', 'address', 'phones', 'email', 'working_hours', 'website', 'last_call_date', 'call_status']
    list_filter = ('call_status', 'visibility')
    search_fields = ['name', 'phones', 'address', 'email', 'about']

    class Media:
        js = ['/static/admin/fckeditor/fckeditor.js', '/static/admin/fckeditor/fckeditor_init.js']

admin.site.register(Clinic, ClinicAdmin)
autocomplete.register(Clinic.region, RegionAutocomplete)
