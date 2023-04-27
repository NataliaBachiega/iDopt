import json
from django.urls import reverse
from rest_framework.test import APITestCase

from idopt.helpers import create_dummy_user
from profiles.models import IdoptUser
from rest_framework import status


class LoginTestCase(APITestCase):
    def setUp(self) -> None:
        create_dummy_user()
        self.url = reverse('login')

    def test_login(self):
        '''
        Simula um usuário fazendo login no iDopt.
        '''

        user = IdoptUser.objects.first()

        payload = {
            'username': user.username,
            'password': '12345678',
            'device': {
                'name': 'Galaxy S23',
                'os': 'Android',
                'os_version': '13',

                # FCM = Firebase Cloud Messaging. Usado para enviar notificações por PUSH.
                'fcm_token': 'Token falso ahahahahahahah'
            }
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=json.dumps(response.data, indent=4)
        )

        self.assertIsInstance(response.data['token'], str)
        self.assertIsInstance(response.data['user'], dict, msg=json.dumps(
            response.data['user'], indent=4))
        self.assertIsInstance(response.data['device'], dict, msg=json.dumps(
            response.data['device'], indent=4))

    def test_invalid_password(self):
        payload = {
            'username': IdoptUser.objects.first().username,
            'password': 'Invalid password',
            'device': {
                'name': 'Galaxy S23',
                'os': 'Android',
                'os_version': '13',

                # FCM = Firebase Cloud Messaging. Usado para enviar notificações por PUSH.
                'fcm_token': 'Token falso ahahahahahahah'
            }
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, json.dumps(
            response.data, indent=4))
