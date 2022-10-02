from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(models.Model):
    """ Represents as single user that's participating in conversations. """
    # TODO: Consider overriding Django's AbstractUser
    pass

class Conversation(models.Model):
    """ Represents a conversation and a good place to put meta-data about the conversation """
    pass


# Trade off here between data-integrity and overall performance (FKs require index locks).
# If we're strictly append-only we should have limited opporutinites to mess up our data.
# Also, in any real scalablility scenario we would likely need to shard the message table which means this
# can't be enabled anyway.
# On the other hand, this would be scary to enable this retroactively for a live db, so might just keep it
# on for as long as it works, especially if we're just running low-volume. *shrugs*
DB_CONSTRAINTS = True

class Message(models.Model):
    """ Represents a single message within a conversation. """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_constraint=DB_CONSTRAINTS)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)

    message_text = models.TextField()

    # Should this be set in the client and passed along for a better user experience?
    sent_at = models.DateTimeField(default=now, blank=True)
    
class UserConversation(models.Model):
    """ Joins users with the conversations they are participating in. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, db_constraint=DB_CONSTRAINTS)
