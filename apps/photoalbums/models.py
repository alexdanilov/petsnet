#-*-coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from apps.fields import StdImageField
from apps.users.models import UserProfile


COMMENT_GROUPS = (
    ('friends', _('friends-users')),
    ('register', _('register-users')),
    ('all', _('all-users')),
)

class Album(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_("user"), db_index=True, null=True, blank=True)
    entity = models.CharField(max_length=32, db_index=True, verbose_name=_("entity"))
    entity_id = models.IntegerField(db_index=True, verbose_name=_("entity_id"))

    name = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.CharField(max_length=255, verbose_name=_('description'))
    
    allow_comments = models.CharField(max_length=10, choices=COMMENT_GROUPS, default='all', verbose_name=_('allow_comments'))
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        db_table = 'photoalbums_albums'
        verbose_name = _("photoalbum")
        verbose_name_plural = _("photoalbums")


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = ('user', 'created')


class Photo(models.Model):
    album = models.ForeignKey(Album, verbose_name=_("album"), db_index=True)

    image = StdImageField(upload_to='p/', verbose_name=_('photo'), sizes=((100, 100), (470, 310), (800, 800)))
    name = models.CharField(max_length=255, verbose_name=_('title'))
    
    comments_count = models.IntegerField(default=0, verbose_name=_('comments_count'), blank=True)
    show_count = models.IntegerField(default=0, verbose_name=_('show_count'), blank=True)
    is_top = models.BooleanField(db_index=True, default=False, verbose_name=_('is_top'))
    created = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return '<img src="/media/p/%s-1.jpg" alt="">' % self.id
    image_url.allow_tags = True

    def __unicode__(self):
        return '/media/p/%s-1.jpg' % self.id

    class Meta:
        ordering = ['-created']
        db_table = 'photoalbums_photos'
        verbose_name = _("photoalbum_photo")
        verbose_name_plural = _("photoalbum_photos")


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'album', 'name', 'is_top', 'comments_count', 'show_count', 'created']
    list_filter = ['is_top', 'created']

admin.site.register(Photo, PhotoAdmin)


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 10


class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    list_display = ['name', 'entity', 'entity_id', 'user', 'allow_comments', 'created']
    list_filter = ['entity', 'allow_comments', 'created']

admin.site.register(Album, AlbumAdmin)


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_("user"), related_name='photo_user_comments', db_index=True)
    photo = models.ForeignKey(Photo, verbose_name=_("photo"), db_index=True)

    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    comment = models.CharField(max_length=255, verbose_name=_("comment"))
    
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return '%s (%s)' % (self.comment, self.user)

    class Meta:
        ordering = ['-created']
        db_table = 'photoalbums_comments'
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'created', 'photo', 'subject')


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'photo', 'user', 'visibility', 'created']
    list_filter = ['visibility', 'created']

admin.site.register(Comment, CommentAdmin)
