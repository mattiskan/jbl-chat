from django.shortcuts import render
from django.http import JsonResponse

from . import models


def index(request):
    return JsonResponse("Tjena världen, från Mattis")

def get_users(request):
    users = list(models.User.objects.values())
    
    return JsonResponse(users, safe=False)

def get_conversation(request):
    messages = list(models.Message.objects.values())
    
    return JsonResponse(messages, safe=False)

def post_message(request):
    user = models.User()
    user.save()

    convo = models.Conversation()
    convo.save()

    userConvo = models.UserConversation(user=user, conversation=convo)
    userConvo.save()

    message = models.Message(conversation=convo, sender=user, message_text="hello world")
    message.save()
    
    return JsonResponse({'id': message.id})
