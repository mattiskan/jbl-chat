from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.get_users, name='get_users'),
    path('conversation', views.list_conversations, name='list_conversations'),
    path('conversation/create', views.create_conversation, name='create_conversation'),
    path('conversation/<int:conversation_id>', views.get_conversation, name='get_conversation'),
    path('conversation/<int:conversation_id>/reply', views.post_reply, name='post_reply'),    
]
