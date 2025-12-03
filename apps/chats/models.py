from django.db import models
from django.conf import settings
from apps.stores.models import Store

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True,)

    class Meta:
        db_table = 'chats'
        unique_together = (('user', 'store'),)

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'messages'