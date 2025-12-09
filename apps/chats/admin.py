from django.contrib import admin
from . import models

@admin.register(models.Chat)
class ChatAmdin(admin.ModelAdmin):
    list_display = ['user', 'store', 'created_at']

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sender', 'created_at', 'is_read']