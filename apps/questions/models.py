#-*-coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from apps.animals.models import AnimalType
from apps.users.models import UserProfile



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('title'))
    
    order_num = models.IntegerField(default=0, verbose_name=_('order_num'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order_num']
        db_table = 'qa_categories'
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Tag(models.Model):
    tag = models.CharField(max_length=255, verbose_name=_('title'), db_index=True)
    count = models.IntegerField(default=0, verbose_name=_('tags_count'))

    def __unicode__(self):
        return self.tag

    class Meta:
        ordering = ['count']
        db_table = 'qa_tags'
        verbose_name = _("tag")
        verbose_name_plural = _("tags")



class Question(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=_("user"), db_index=True)
    animal_type = models.ForeignKey(AnimalType, verbose_name=_("animal_type"), blank=True, null=True, db_index=True)
    category = models.ForeignKey(Category, verbose_name=_("user"), blank=True, db_index=True, null=True)
    
    title = models.CharField(max_length=255, verbose_name=_('title'))
    text = models.TextField(verbose_name=_('description'))
    answers_count = models.IntegerField(default=0, verbose_name=_('comments_count'), blank=True)
    
    show_count = models.IntegerField(default=0, verbose_name=_('show_count'), blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    @property
    def url(self):
        return '/questions/%s' % self.id

    class Meta:
        ordering = ['-created']
        db_table = 'qa_questions'
        verbose_name = _("question")
        verbose_name_plural = _("questions")


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['user', 'tags', 'created', 'answers_count', 'show_count']



class Answer(models.Model):
    parent = models.ForeignKey('self', verbose_name=_("parent"), db_index=True, blank=True, null=True)
    user = models.ForeignKey(UserProfile, verbose_name=_("user"), related_name='qa_user_comments', db_index=True)
    question = models.ForeignKey(Question, verbose_name=_("question"), db_index=True)
    
    text = models.CharField(max_length=500, verbose_name=_("answer"))
    
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    def __unicode__(self):
        return '%s' % self.text

    class Meta:
        ordering = ['created']
        db_table = 'qa_answers'
        verbose_name = _("answer")
        verbose_name_plural = _("answers")


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ('user', 'created')



# Admin classes
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order_num']

admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'answers_count', 'created']
    search_fields = ['title']

admin.site.register(Question, QuestionAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'count']
    list_filter = ('count', )

admin.site.register(Tag, TagAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'parent', 'created']

admin.site.register(Answer, AnswerAdmin)

