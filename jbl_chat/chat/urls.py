from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.get_users, name='get_users'),
    path('conversation', views.get_conversation, name='get_conversation'),
    path('message', views.post_message, name='post_message'),    
]
