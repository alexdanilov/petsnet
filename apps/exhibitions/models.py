from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from tinymce import models as tinymce_models

from apps.system.models import Regions



EXHIBITIONS_TYPES = (
    ('cats', _('exhibitions-cats')),
    ('dogs', _('exhibitions-dogs')),
)
class Exhibition(models.Model):
    region = models.ForeignKey(Regions, verbose_name=_("region"), db_index=True)
    type = models.CharField(max_length=16, choices=EXHIBITIONS_TYPES, verbose_name=_("type"), db_index=True)

    name = models.CharField(max_length=255, verbose_name=_("name"))
    website = models.URLField(max_length=255, verbose_name=_("website"), blank=True)
    email = models.EmailField(max_length=255, verbose_name=_("email"), blank=True)
    address = models.CharField(max_length=255, verbose_name=_("address"))
    phones = models.CharField(max_length=255, verbose_name=_("phones"), blank=True)

    begin_date = models.DateField(verbose_name=_("begin_date"), db_index=True)
    end_date = models.DateField(verbose_name=_("end_date"), db_index=True)
    organizator = models.CharField(max_length=255, verbose_name=_("organizator"))
    enter_price = models.CharField(max_length=255, verbose_name=_("enter_price"), default=0)
    system = models.CharField(max_length=255, verbose_name=_("system"))
    about = tinymce_models.HTMLField(verbose_name=_("description"))
    program = tinymce_models.HTMLField(verbose_name=_("program"))
    experts = tinymce_models.HTMLField(verbose_name=_("experts"))

    visibility = models.BooleanField(default=True, verbose_name=_("visibility"), db_index=True)

    @property
    def phones_list(self):
        return self.phones.split(',')

    @property
    def url(self):
        return '/exhibitions/%s' % self.id

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['begin_date']
        db_table = 'catalog_exhibitions'
        verbose_name = _("exhibition")
        verbose_name_plural = _("exhibitions")



# Admin classes
class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city',)


class ExhibitionAdmin(AutocompleteAdmin, admin.ModelAdmin):
    list_display = ['name', 'type', 'region', 'begin_date', 'end_date', 'address', 'phones', 'email', 'website']
    list_filter = ['type']
    search_fields = ['name', 'email', 'phones', 'address']

admin.site.register(Exhibition, ExhibitionAdmin)
autocomplete.register(Exhibition.region, RegionAutocomplete)
