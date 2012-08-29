from django.contrib import admin
from apps.system.models import *


class BannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'visibility']

admin.site.register(Banner, BannerAdmin)


class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'subject']

admin.site.register(MailTemplate, MailTemplateAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'created', 'visibility']
    list_filter = ('visibility',)

admin.site.register(Page, PageAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'value']

admin.site.register(Setting, SettingAdmin)


class TextblockAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

admin.site.register(Textblock, TextblockAdmin)
