from django.urls import path, re_path
from . import views
# from . import consumers

app_name = 'chats'

urlpatterns = [
    path('', views.chat, name='chat'),
    path('list/', views.chat_list, name='list'),
    path('<int:chat_id>/', views.chat_area, name='area')
]

# websocket_urlpatterns = [
#     # Captura o chat_id da URL
#     re_path(r"ws/chat/(?P<chat_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
# ]