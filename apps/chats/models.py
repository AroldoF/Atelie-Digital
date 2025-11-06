from django.db import models
from apps.accounts.models import Users
from apps.stores.models import Stores

class Chats(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, related_name='chats', on_delete=models.CASCADE)
    store = models.ForeignKey(Stores, related_name='chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True,)

    class Meta:
        managed = False
        db_table = 'chats'
        unique_together = (('user', 'store'),)

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'