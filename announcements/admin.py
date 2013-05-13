from django.contrib import admin
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from announcements.models import *


# Auto completes
class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city_name_ru', '^city_name_en')


class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'items_count']

admin.site.register(AnnouncementCategory, AnnouncementCategoryAdmin)


class AnnouncementImageInline(admin.TabularInline):
    model = AnnouncementImage
    extra = 5

class AnnouncementAdmin(AutocompleteAdmin, admin.ModelAdmin):
    inlines = [AnnouncementImageInline, ]
    list_display = ['title', 'category', 'user', 'region', 'price', 'show_count', 'phone', 'end_date']
    list_filter = ['category', 'type', 'is_top', 'is_border']
    search_fields = ['title']

admin.site.register(Announcement, AnnouncementAdmin)
autocomplete.register(Announcement.region, RegionAutocomplete)
