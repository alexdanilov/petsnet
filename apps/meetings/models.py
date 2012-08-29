from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin

from apps.system.models import Regions
from apps.users.models import UserProfile


class Meeting(models.Model):
    region = models.ForeignKey(Regions, verbose_name=_("region"), db_index=True)
    user = models.ForeignKey(UserProfile, verbose_name=_("owner"), db_index=True)

    name = models.CharField(max_length=255, verbose_name=_("name"))
    address = models.CharField(max_length=255, verbose_name=_("address"))
    begin_time = models.CharField(max_length=255, verbose_name=_("begin_time"))
    begin_date = models.DateField(verbose_name=_("begin_date"), db_index=True)
    end_date = models.DateField(verbose_name=_("end_date"), db_index=True)
    description = models.TextField(verbose_name=_("description"))

    allow_comments = models.BooleanField(default=True, verbose_name=_('allow_comments'))
    show_count = models.IntegerField(default=0, verbose_name=_('show_count'))
    comments_count = models.IntegerField(default=0, verbose_name=_('comments_count'))
    members_count = models.IntegerField(default=0, verbose_name=_('members_count'))
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
        ordering = ['begin_date']
        db_table = 'catalog_meetings'
        verbose_name = _("meeting")
        verbose_name_plural = _("meetings")


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ('user', 'comments_count', 'show_count', 'members_count')


class MeetingMember(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_("member"), db_index=True)
    meeting = models.ForeignKey(Meeting, verbose_name=_("meeting"), db_index=True)

    def __unicode__(self):
        return self.meeting

    class Meta:
        db_table = 'catalog_meetings_members'
        verbose_name = _("meetings_member")
        verbose_name_plural = _("meetings_members")


# Admin classes
class RegionAutocomplete(AutocompleteSettings):
    search_fields = ('^city',)


class MeetingAdmin(AutocompleteAdmin, admin.ModelAdmin):
    list_display = ['name', 'region', 'user', 'begin_date', 'begin_time', 'end_date', 'address']
    search_fields = ['name', 'address']

admin.site.register(Meeting, MeetingAdmin)
autocomplete.register(Meeting.region, RegionAutocomplete)

