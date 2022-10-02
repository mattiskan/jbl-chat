import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


from . import models

@require_http_methods(["GET"])
def index(request):
    return JsonResponse("Tjena världen, från Mattis")


@require_http_methods(["GET"])
def get_users(request):
    users = list(models.User.objects.values())
    
    return JsonResponse(users, safe=False)

@require_http_methods(["GET"])
def list_conversations(request):
    current_user = models.User.objects.first() # todo -- look up from session
    
    conversations = [x.conversation_id for x in models.UserConversation.objects.filter(user_id=current_user)]
    return JsonResponse(list(conversations), safe=False)

@require_http_methods(["GET"])
def get_conversation(request, conversation_id):
    return JsonResponse({})


@require_http_methods(["POST"])
def post_message(request):

    # todo: try/catch
    print(request.body)
    params = json.loads(request.body)

    current_user = models.User.objects.first() # todo -- look up from session

    convo = models.Conversation()
    convo.save()

    userConvo = models.UserConversation(user=current_user, conversation=convo)
    userConvo.save()

    message = models.Message(conversation=convo, sender=current_user, message_text="hello world")
    message.save()
    
    return JsonResponse({'id': message.id})
