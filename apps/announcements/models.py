#-*-coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from apps.system.models import Region
from apps.users.models import UserProfile
from apps.fields import StdImageField


class AnnouncementCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    
    items_count = models.IntegerField()

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.items_count)

    class Meta:
        db_table = 'announcements_categories'
        verbose_name = _("announcement-category")
        verbose_name_plural = _("announcement-categories")


TYPE_CHOICES = (
    (u'sale', _('announcements-sale')),
    (u'buy', _('announcements-buy')),
    (u'coupling', _('announcements-coupling')),
    (u'take-free', _('announcements-take-free')),
    (u'give-free', _('announcements-give-free')),
    (u'other', _('Other')),
)
TYPE_CHOICES_DICT = dict(TYPE_CHOICES)


class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))
    address = models.CharField(max_length=255, verbose_name=_("address"), blank=True)
    phone = models.CharField(max_length=255, verbose_name=_("phone"), blank=True)
    price = models.IntegerField(verbose_name=_("price"), blank=True, default=0)
    
    show_count = models.IntegerField(default=0, editable=False, blank=True)
    is_top = models.BooleanField(default=False, verbose_name=_("is_top"), blank=True)
    is_border = models.BooleanField(default=False, verbose_name=_("is_border"), blank=True)
    end_date = models.DateField(verbose_name=_("end_date"))
    
    created = models.DateTimeField(auto_now_add=True)
    visibility = models.BooleanField(default=True, verbose_name=_("visibility"))
    deleted = models.BooleanField(default=False, verbose_name=_("deleted"))
    
    user = models.ForeignKey(UserProfile, verbose_name=_("user"))
    region = models.ForeignKey(Region, verbose_name=_("region"))
    category = models.ForeignKey(AnnouncementCategory, verbose_name=_("announcement-category"))
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, verbose_name=_("type"))

    @property
    def type_name(self):
        return TYPE_CHOICES_DICT.get(self.type)
    
    @property
    def images(self):
        return AnnouncementImage.objects.filter(announcement=self)

    @property
    def image(self):
        try:
            image = AnnouncementImage.objects.filter(announcement=self)[0].image.image1
        except Exception:
            image = None
        return image
    
    @property
    def url(self):
        return '/announcements/%s' % self.id

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        db_table = 'announcements_announcements'
        verbose_name = _("announcement")
        verbose_name_plural = _("announcements")


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'region', 'category', 'price', 'description', 'address', 'type', 'phone')


class AnnouncementImage(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image = StdImageField(upload_to='an/', verbose_name=_('photo'), sizes=((100, 100), (200, 200), (500, 500)))
    
    announcement = models.ForeignKey(Announcement, verbose_name=_('image'))

    def __unicode__(self):
        return 'an/%s-1.jpg' % self.id

    class Meta:
        db_table = 'announcements_images'
        verbose_name = _("announcements_image")
        verbose_name_plural = _("announcements_image")
