from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

from system.models import Region


class Pharmacy(models.Model):
    region = models.ForeignKey(Region, verbose_name=_("region"), db_index=True)

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    address = models.CharField(max_length=255, verbose_name=_("address"))
    phones = models.CharField(max_length=255, verbose_name=_("phones"), blank=True)
    website = models.URLField(max_length=255, verbose_name=_("website"), blank=True)
    email = models.EmailField(max_length=255, verbose_name=_("email"), blank=True)
    
    working_hours = models.CharField(max_length=64, verbose_name=_("working_hours"), blank=True)
    working_hours_saturday = models.CharField(max_length=64, verbose_name=_("working_hours_saturday"), blank=True)
    working_hours_sanday = models.CharField(max_length=64, verbose_name=_("working_hours_sanday"), blank=True)

    is_top = models.BooleanField(default=False, verbose_name=_("is_top"))
    is_sale = models.BooleanField(default=False, verbose_name=_("is_sale"))

    order_num = models.IntegerField(verbose_name=_("order_num"))
    visibility = models.BooleanField(default=True, verbose_name=_("visibility"), db_index=True)

    @property
    def phones_list(self):
        return self.phones.split(',')

    @property
    def url(self):
        return '/pharmacies/%s' % self.id

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order_num']
        db_table = 'pharmacies'
        verbose_name = _("pharmacy")
        verbose_name_plural = _("pharmacies")


# Admin classes
class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city',)


class PharmacyAdmin(AutocompleteAdmin, admin.ModelAdmin):
    list_display = ['name', 'region', 'address', 'phones', 'email', 'working_hours', 'website', 'order_num']
    search_fields = ['name', 'email', 'phones', 'address']

admin.site.register(Pharmacy, PharmacyAdmin)
autocomplete.register(Pharmacy.region, RegionAutocomplete)
