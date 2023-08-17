from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Profile)
class ProfileAdmin (admin.ModelAdmin):
    list_display = ['user', 'avatar', 'first_name', 'last_name', 'work', 'bio', 'stage']
    filter_horizontal = ('tags', )


@admin.register(Worksheet)
class WorksheetsAdmin (admin.ModelAdmin):
    list_display = ['title', 'image', 'author', 'description', 'date']
    filter_horizontal = ('tags', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'color', 'description']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['profile']
    filter_horizontal = ('contacts', )


@admin.register(SocialMedia)
class SocialMediaAdmin (admin.ModelAdmin):
    list_display = ['profile', 'instagram', 'vk', 'github', 'codewars']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'author', 'recipient', 'is_checked']


@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin):
    list_display = ['text_message', 'author', 'worksheet']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'worksheet']


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'worksheet']
