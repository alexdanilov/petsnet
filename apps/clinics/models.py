from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

from tinymce import models as tinymce_models
from apps.system.models import Regions


class ClinicService(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'catalog_clinic_services'
        verbose_name = _("clinic-service")
        verbose_name_plural = _("clinic-services")


class Clinic(models.Model):
    region = models.ForeignKey(Regions, verbose_name=_("region"), db_index=True)

    name = models.CharField(max_length=255, verbose_name=_("name"))
    about = tinymce_models.HTMLField(verbose_name=_("description"))
    address = models.CharField(max_length=255, verbose_name=_("address"))
    phones = models.CharField(max_length=255, verbose_name=_("phones"))
    working_hours = models.CharField(max_length=64, verbose_name=_("working_hours"), blank=True)
    website = models.URLField(max_length=255, verbose_name=_("website"), blank=True)
    email = models.EmailField(max_length=255, verbose_name=_("email"), blank=True)

    services = models.ManyToManyField(ClinicService, verbose_name=_("clinic-services"))
    prices = tinymce_models.HTMLField(verbose_name=_("prices"), blank=True)
    coworkers = tinymce_models.HTMLField(verbose_name=_("coworkers"))

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
        db_table = 'catalog_clinics'
        verbose_name = _("clinic")
        verbose_name_plural = _("clinics")


# Admin classes
class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city',)


class ClinicServiceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(ClinicService, ClinicServiceAdmin)


class ClinicAdmin(AutocompleteAdmin, admin.ModelAdmin):
    list_display = ['name', 'region', 'address', 'phones', 'email', 'working_hours', 'website', 'order_num']
    #list_filter = ('category', 'type', 'is_top', 'is_border')

admin.site.register(Clinic, ClinicAdmin)
autocomplete.register(Clinic.region, RegionAutocomplete)
