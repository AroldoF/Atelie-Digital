from django.contrib import admin
from . import models

class MessageInline(admin.TabularInline):
    model = models.Message
    extra = 1

@admin.register(models.Chat)
class ChatAmdin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = ['user', 'store', 'created_at']

# @admin.register(models.Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'sender', 'created_at', 'is_read']