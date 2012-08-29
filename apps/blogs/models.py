#-*-coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from apps.users.models import UserProfile


COMMENT_GROUPS = (
    ('friends', _('friends-users')),
    ('register', _('register-users')),
    ('all', _('all-users')),
)

class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.CharField(max_length=255, verbose_name=_('description'))
    allow_comments = models.CharField(max_length=10, choices=COMMENT_GROUPS, default='all', verbose_name=_('allow_comments'))
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        db_table = 'blogs_blogs'
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")



class Tag(models.Model):
    tag = models.CharField(max_length=255, verbose_name=_('title'))
    count = models.IntegerField(default=0, verbose_name=_('tags_count'))

    def __unicode__(self):
        return self.tag

    class Meta:
        ordering = ['count']
        db_table = 'blogs_tags'
        verbose_name = _("tag")
        verbose_name_plural = _("tags")



class Post(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_("user"), db_index=True)
    blog = models.ForeignKey(Blog, verbose_name=_("blog"), blank=True, db_index=True, null=True)
    title = models.CharField(max_length=255, verbose_name=_('title'))
    text = models.TextField(verbose_name=_('description'))
    allow_comments = models.CharField(max_length=10, choices=COMMENT_GROUPS, default='all', verbose_name=_('allow_comments'))
    comments_count = models.IntegerField(default=0, verbose_name=_('comments_count'), blank=True)
    show_count = models.IntegerField(default=0, verbose_name=_('show_count'), blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        db_table = 'blogs_posts'
        verbose_name = _("post")
        verbose_name_plural = _("posts")


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'created', 'tags', 'blog', 'comments_count', 'show_count')



class Comment(models.Model):
    site_id = models.IntegerField(verbose_name=_("site"))
    user = models.ForeignKey(UserProfile, verbose_name=_("user"), related_name='blog_user_comments', db_index=True)
    post = models.ForeignKey(Post, verbose_name=_("post"), db_index=True)
    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    comment = models.CharField(max_length=255, verbose_name=_("comment"))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return '%s (%s)' % (self.comment, self.user)

    class Meta:
        ordering = ['-created']
        db_table = 'blogs_comments'
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'created', 'site_id', 'post', 'subject')
