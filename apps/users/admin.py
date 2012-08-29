from django.contrib import admin
from apps.users.models import *



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'gender', 'balance', 'balls', 'birth_day']
    list_filter = ('gender',)

admin.site.register(UserProfile, UserProfileAdmin)



class UserFriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'accept', 'created']
    list_filter = ('accept',)

admin.site.register(UserFriend, UserFriendAdmin)



class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'author', 'subject', 'readed', 'created']
    list_filter = ('readed',)

admin.site.register(UserMessage, UserMessageAdmin)


class UserWallAdmin(admin.ModelAdmin):
    list_display = ['user', 'author', 'message', 'created']

admin.site.register(UserWall, UserWallAdmin)
