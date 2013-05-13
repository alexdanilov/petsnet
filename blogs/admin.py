from django.contrib import admin
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from blogs.models import *



class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'allow_comments', 'created']
    list_filter = ('allow_comments', )

admin.site.register(Blog, BlogAdmin)



class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'title', 'allow_comments', 'comments_count', 'created']
    list_filter = ('allow_comments', )

admin.site.register(Post, PostAdmin)



class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'count']
    list_filter = ('count', )

admin.site.register(Tag, TagAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'subject', 'comment', 'created', 'visibility']
    list_filter = ('visibility', )

admin.site.register(Comment, CommentAdmin)
