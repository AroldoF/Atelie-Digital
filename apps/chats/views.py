from django.shortcuts import render
from django.views import View

class ChatView(View):
    def get(self, request):
        return render(request, 'chats/chats.html')