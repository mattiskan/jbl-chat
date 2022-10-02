from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return JsonResponse("Tjena världen, från Mattis")



user = {
    'id': 3,
    'name': 'Ben'
}

message = {
    'id': 123,
    'sent_time': '2020-03-20T14:28:23.382748',
    'text': 'Hi there, how are you?'
}


def get_users(request):
    return JsonResponse({
        'users': [user] * 3,
    })

def get_conversation(request):
    return JsonResponse({
        'recipient': user,
        'conversation': [message] * 3,
    })

def post_message(request):
    return JsonResponse({})
