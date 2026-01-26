from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.db.models import Q, Prefetch
from apps.accounts.models import Profile

@login_required
def chat(request):
    user = request.user

    chats = (
        Chat.objects
        .filter(Q(client=user) | Q(artisan=user))
        .select_related("client", "artisan")
        .prefetch_related(
            "client__profile",
            "artisan__stores",
        )
    )

    chat_list = []

    for chat in chats:
        # define quem é o outro usuário
        if chat.client == user:
            other_user = chat.artisan
        else:
            other_user = chat.client

        chat_list.append({
            "chat": chat,
            "other_user": other_user,
        })

    return render(
        request,
        "chats/chats.html",
        {"chat_list": chat_list}
    )


@login_required
def chat_area(request, chat_id):
    chat = get_object_or_404(Chat.objects.prefetch_related(
        "client__profile",
        "artisan__stores",
    ), pk=chat_id)
    
    messages = Message.objects.filter(chat=chat).order_by('created_at')

    if chat.client == request.user:
        other_user = chat.artisan
    else:
        other_user = chat.client

    return render(request, 'chats/partials/area.html', {'chat': chat, "other_user": other_user, 'messages': messages})
    
@login_required
def send_message(request):
    return render(request, 'template/partials/message.html')