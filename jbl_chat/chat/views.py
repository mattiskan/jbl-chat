import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods


from . import models

@require_http_methods(["GET"])
def index(request):
    return JsonResponse({"msg": "Tjena världen, från Mattis"})


@require_http_methods(["GET"])
def get_users(request):
    users = list(models.User.objects.values())
    
    return JsonResponse(users, safe=False)

@require_http_methods(["GET"])
def list_conversations(request):
    current_user, error = _user_from_session(request)
    if error:
        return error
    
    conversations = [x.conversation_id for x in models.UserConversation.objects.filter(user_id=current_user)]
    return JsonResponse(list(conversations), safe=False)

@require_http_methods(["GET"])
def get_conversation(request, conversation_id):
    current_user, error = _user_from_session(request)
    if error:
        return error
    
    participants = [
        uc.user_id
        for uc
        in models.UserConversation.objects.filter(conversation_id=conversation_id)
    ]

    if not current_user.id in participants:
        return HttpResponseForbidden()

    messages = models.Message.objects.filter(conversation=conversation_id).values()
    
    return JsonResponse({
        'participants': list(participants),
        'messages': list(messages),
    })


@require_http_methods(["POST"])
def post_message(request):

    # todo: try/catch
    params = json.loads(request.body)

    current_user, error = _user_from_session(request)
    if error:
        return error

    convo = models.Conversation()
    convo.save()

    sender = models.UserConversation(user=current_user, conversation=convo)
    sender.save()

    recipient = models.UserConversation(
        user=models.User.objects.filter(pk=params['recipient'])[0],
        conversation=convo,
    )
    recipient.save()

    message = models.Message(
        conversation=convo,
        sender=current_user,
        message_text=params['text'],
    )
    message.save()
    
    return JsonResponse({'id': message.id})



def _user_from_session(request):
    session_token = request.headers.get('SESSION_TOKEN')

    if not session_token:
        return None, HttpResponseForbidden('Invalid session')


    # TODO: Introduce session tokens and look up user for session
    # for now I'm just passing the user-id I want

    users = models.User.objects.filter(pk=session_token) # todo -- look up from session
    if not users:
        return None, HttpResponseForbidden('Invalid session')

    return users[0], None
