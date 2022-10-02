from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(models.Model):
    pass

class Conversation(models.Model):
    pass

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_constraint=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)

    message_text = models.TextField()
    sent_at = models.DateTimeField(default=now, blank=True)
    
class UserConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_constraint=False)
