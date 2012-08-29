#-*-coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.users.models import UserProfile


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(max_length=255, verbose_name=_("slug"))
    description = models.TextField(verbose_name=_("description"))
    items_count = models.IntegerField(default=0, verbose_name=_("items_count"))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']
        db_table = 'content_categories'
        verbose_name = _("category")
        verbose_name_plural = _("categories")

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'items_count', 'visibility']
    list_filter = ('visibility',)

admin.site.register(ArticleCategory, ArticleCategoryAdmin)



class Article(models.Model):
    category = models.ForeignKey(ArticleCategory, verbose_name=_("category"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(max_length=255, verbose_name=_("slug"))
    description = models.TextField(verbose_name=_("description"))
    body = models.TextField(verbose_name=_("body"))
    page_title = models.CharField(max_length=255, verbose_name=_("page_title"))
    page_description = models.CharField(max_length=255, verbose_name=_("page_description"))
    page_keywords = models.TextField(verbose_name=_("page_keywords"))
    comments_count = models.IntegerField(default=0, verbose_name=_("comments_count"))
    allow_comment = models.BooleanField(default=True, verbose_name=_("allow_comment"))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.category)

    class Meta:
        ordering = ['-created']
        db_table = 'content_articles'
        verbose_name = _("article")
        verbose_name_plural = _("articles")

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'created', 'visibility']
    list_filter = ('category', 'visibility')

admin.site.register(Article, ArticleAdmin)



class Comment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_("user"))
    entity = models.CharField(max_length=32, db_index=True, verbose_name=_("entity"))
    id_entities = models.IntegerField(db_index=True, verbose_name=_("entity_id"))
    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    comment = models.CharField(max_length=255, verbose_name=_("comment"))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return '%s (%s)' % (self.comment, self.user)

    class Meta:
        ordering = ['-created']
        db_table = 'content_comments'
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'entity', 'subject', 'comment', 'created', 'visibility']
    list_filter = ('entity', 'visibility')

admin.site.register(Comment, CommentAdmin)



class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(max_length=255, verbose_name=_("slug"))
    description = models.TextField(verbose_name=_("description"))
    body = models.TextField(verbose_name=_("body"))
    page_title = models.CharField(max_length=255, verbose_name=_("page_title"))
    page_description = models.CharField(max_length=255, verbose_name=_("page_description"))
    page_keywords = models.TextField(verbose_name=_("page_keywords"))
    visibility = models.BooleanField(default=True, db_index=True, verbose_name=_("visibility"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        db_table = 'content_pages'
        verbose_name = _("page")
        verbose_name_plural = _("pages")

class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'created', 'visibility']
    list_filter = ('visibility',)

admin.site.register(Page, PageAdmin)
