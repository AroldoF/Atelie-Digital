from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client_chats', on_delete=models.CASCADE)
    artisan = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='artisan_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat {self.client} ↔ {self.artisan}'
    
    def clean(self):
        super().clean()
        if self.client == self.artisan:
            raise ValidationError("Client and Artisan cannot be the same user")
        
    
    class Meta:
        db_table = 'chats'
        unique_together = (('client', 'artisan'),)

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} - {self.created_at}'

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
