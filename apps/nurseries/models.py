#-*-coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

from tinymce import models as tinymce_models
from apps.fields import StdImageField
from apps.system.models import Region
from apps.animals.models import Breed



class NurseryService(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'nursery_services'
        verbose_name = _("nursery-service")
        verbose_name_plural = _("nursery-services")


NURSERIES_TYPES = (
    ('cats', _('nurseries-cats')),
    ('dogs', _('nurseries-dogs')),
)
NURSERIES_TYPES_DICT = dict(NURSERIES_TYPES)

CALL_STATUSES = (
    ('call', u'Позвонить'),
    ('recall', u'Перезвонить'),
    ('called', u'Уже позвонили'),
)
class Nursery(models.Model):
    region = models.ForeignKey(Region, verbose_name=_("region"), blank=True, db_index=True)
    type = models.CharField(max_length=16, choices=NURSERIES_TYPES, verbose_name=_("type"), db_index=True)

    name = models.CharField(max_length=255, verbose_name=_("name"))
    website = models.URLField(max_length=255, verbose_name=_("website"), blank=True)
    email = models.EmailField(max_length=255, verbose_name=_("email"), blank=True)
    address = models.CharField(max_length=255, verbose_name=_("address"), blank=True)
    phones = models.CharField(max_length=255, verbose_name=_("phones"))
    description = tinymce_models.HTMLField(verbose_name=_("description"))

    breeds = models.ManyToManyField(Breed, verbose_name=_("breeds"), blank=True)
    services = models.ManyToManyField(NurseryService, verbose_name=_("nursery-services"))

    owner = models.CharField(max_length=255, verbose_name=_("owner"), blank=True)
    system = models.CharField(max_length=255, verbose_name=_("system"), blank=True)
    children = models.CharField(max_length=255, verbose_name=_("nurseries-children"), blank=True)

    is_top = models.BooleanField(default=False, verbose_name=_("is_top"))
    is_sale = models.BooleanField(default=False, verbose_name=_("is_sale"))
    
    last_call_date = models.DateTimeField(verbose_name=_("last_call_date"), blank=True)
    call_status = models.CharField(max_length=10, verbose_name=_('call_status'), choices=CALL_STATUSES)

    order_num = models.IntegerField(verbose_name=_("order_num"))
    visibility = models.BooleanField(default=True, verbose_name=_("visibility"), db_index=True)

    def __unicode__(self):
        return self.name

    @property
    def images_list(self):
        return NurseryImage.objects.filter(nursery=self)

    @property
    def image(self):
        try:
            img = self.images_list[0].image.image1
        except Exception:
            img = None
        return img

    @property
    def url(self):
        return '/nurseries/%s' % self.id

    @property
    def phones_list(self):
        return self.phones.split(',')

    def type_name(self):
        return NURSERIES_TYPES_DICT.get(self.type)

    class Meta:
        ordering = ['order_num']
        db_table = 'nurseries'
        verbose_name = _("nursery")
        verbose_name_plural = _("nurseries")


class NurseryImage(models.Model):
    nursery = models.ForeignKey(Nursery, related_name='images')
    image = StdImageField(upload_to='n/', blank=True, sizes=((100, 100), (180, 180), (640, 480)))
    name = models.CharField(max_length=255, verbose_name=_("name"), blank=True)
    order_num = models.IntegerField(verbose_name=_("order_num"), blank=True, default=0)

    class Meta:
        ordering = ['order_num']
        db_table = 'nurseries_images'
        verbose_name = _("image")


# Admin classes
class BreedAutocomplete(AutocompleteSettings):
    search_fields = ('^name',)


class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city',)


class NurseryServiceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(NurseryService, NurseryServiceAdmin)


class NurseryImageInline(admin.TabularInline):
    model = NurseryImage
    extra = 10


class NurseryAdmin(AutocompleteAdmin, admin.ModelAdmin):
    class Media:
        js = ['/js/admin.js', ]
    inlines = [NurseryImageInline, ]
    list_display = ['name', 'type', 'region', 'address', 'phones', 'email', 'website', 'last_call_date', 'call_status']
    list_filter = ['type', 'call_status']
    search_fields = ['name', 'phones', 'address', 'email', 'about']

    class Media:
        js = ['/static/admin/fckeditor/fckeditor.js', '/static/admin/fckeditor/fckeditor_init.js']

admin.site.register(Nursery, NurseryAdmin)
autocomplete.register(Nursery.breeds, BreedAutocomplete)
autocomplete.register(Nursery.region, RegionAutocomplete)
