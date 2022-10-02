from django.test import TestCase
from unittest import mock
from contextlib import contextmanager

from chat import models


class ChatViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.number_of_users = 3

        for user_id in range(cls.number_of_users):
            models.User.objects.create()

    def test_list_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.number_of_users)

    # NOTE: I would probably recommend separating this test into parts with
    # individual setups and not running them in a long sequence
    def test_create_new_message_thread(self):
        # Premise: No preexisting conversations
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


        # Action: Send a message to create a conversation
        with mock_message_sent_at():
            response = self.client.post(
                '/message',
                {'text': 'hello world, this is test', 'recipient': 2},
                content_type="application/json",
                HTTP_SESSION_TOKEN='1'
            )
        self.assertEqual(response.status_code, 200)

        # Assetion: Expect new conversation to exist
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='1')
        self.assertEqual(response.status_code, 200)

        convo, = response.json() # exactly length one or fail

        response = self.client.get(f'/conversation/{convo}', HTTP_SESSION_TOKEN='1')
        self.assertEqual(response.status_code, 200)        
        self.assertEqual(response.json(), {
            "participants": [1, 2],
            "messages": [
                {
                    "id": 1,
                    "conversation_id": 1,
                    "message_text": "hello world, this is test",
                    "sender_id": 1,
                    "sent_at": '2022-10-02T14:58:39.569Z',                    
                },
            ],
        })

        # Assertion: User 2 can also see the conversation
        response = self.client.get(f'/conversation/{convo}', HTTP_SESSION_TOKEN='2')
        self.assertEqual(response.status_code, 200)

        # Assertion: Non-participant user cannot see and cannot access the conversation in question
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        
        response = self.client.get(f'/conversation/{convo}', HTTP_SESSION_TOKEN='3')
        self.assertEqual(response.status_code, 403)
        



@contextmanager
def mock_message_sent_at():
    field = models.Message._meta.get_field('sent_at')
    mock_now = '2022-10-02T14:58:39.569Z'
    with mock.patch.object(field, 'default', new=mock_now):
        yield
