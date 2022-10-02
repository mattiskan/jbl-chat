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

    def test_create_and_reply_to_conversation(self):
        """ Tests the main use-case:
            * Test that a user can create a new conversation
            * Tests that another user can reply to the conversation
            * Tests that other users can't see a conversation they are not invited to.

        If there would be active development and/or many authors working on this I would consider
        breaking it into separate tests with individual setups (via helper functions) to provide
        more clarity for devs what specifically is breaking rather than just "something is wrong"
        and also to provide an abstraction between tested code's intefrace and the test itself.
        """
        
        # Premise: No preexisting conversations
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        # Action: Send a message to create a conversation
        with mock_message_sent_at('2022-10-02T14:58:39.569Z'):
            response = self.client.post(
                '/conversation/create',
                {'text': 'hello world, this is test', 'participants': [2]},
                content_type="application/json",
                HTTP_SESSION_TOKEN='1'
            )
        self.assertEqual(response.status_code, 200)

        # Assetion: Expect new conversation to exist
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='1')
        self.assertEqual(response.status_code, 200)

        conversation_id, = response.json() # exactly length one or fail

        response = self.client.get(f'/conversation/{conversation_id}', HTTP_SESSION_TOKEN='1')
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
        response = self.client.get(f'/conversation/{conversation_id}', HTTP_SESSION_TOKEN='2')
        self.assertEqual(response.status_code, 200)

        # Assertion: Non-participant user cannot see and cannot access the conversation in question
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        
        response = self.client.get(f'/conversation/{conversation_id}', HTTP_SESSION_TOKEN='3')
        self.assertEqual(response.status_code, 403)


        # Action: Second user replies to existing conversation

        with mock_message_sent_at('2022-10-02T15:00:00.000Z'):
            response = self.client.post(
                f'/conversation/{conversation_id}/reply',
                {'text': 'Hello test! This is world!'},
                content_type="application/json",
                HTTP_SESSION_TOKEN='2'
            )
        self.assertEqual(response.status_code, 200)

        # Assetion: Expect conversation id to be consistent and to have response
        response = self.client.get('/conversation', HTTP_SESSION_TOKEN='2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(conversation_id in response.json())

        response = self.client.get(f'/conversation/{conversation_id}', HTTP_SESSION_TOKEN='2')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            "participants": [1, 2],
            "messages": [
                {
                    "id": 1,
                    "conversation_id": conversation_id,
                    "message_text": "hello world, this is test",
                    "sender_id": 1,
                    "sent_at": '2022-10-02T14:58:39.569Z',
                },
                {
                    "id": 2,
                    "conversation_id": conversation_id,
                    "message_text": "Hello test! This is world!",
                    "sender_id": 2,
                    "sent_at": '2022-10-02T15:00:00Z',
                },                
            ],
        })

    # TODO: Test the "usual suspects" like bad params, users that don't exist, etc.
        

@contextmanager
def mock_message_sent_at(ts):
    field = models.Message._meta.get_field('sent_at')
    mock_now = ts
    with mock.patch.object(field, 'default', new=mock_now):
        yield
