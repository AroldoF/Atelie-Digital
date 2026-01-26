# apps/chats/consumers.py
import json
from asgiref.sync import async_to_sync 
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from .models import Chat, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Correção: Usamos async_to_sync para funções do Channels
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('chat_message')
        user = self.scope['user']

        if message_text:
            chat = Chat.objects.get(pk=self.chat_id)

            message = Message.objects.create(
                chat=chat,
                sender=user,
                content=message_text
            )

            context = {'msg': message, 'user': user ,"is_websocket": True}
            html = render_to_string('chats/partials/message.html', context)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'html': html
                }
            )

    def chat_message(self, event):
        self.send(text_data=event['html'])