from django.test import TestCase

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

    def test_list_conversations_for_user(self):
        # Premise: No preexisting conversations
        response = self.client.get('/conversation')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


        # Action: Send a message to create a conversation
        response = self.client.post(
            '/message',
            {'message': 'hello world, this is test', 'recipient': 2},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Assetion: Expect new conversation to exist
        response = self.client.get('/conversation')
        self.assertEqual(response.status_code, 200)

        convo, = response.json() # exactly length one or fail

        response = self.client.get(f'/conversation/{convo}')
        self.assertEqual(response.status_code, 200)        
        self.assertEqual(response.json(), {})


        
        
