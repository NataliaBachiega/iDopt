import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from idopt.helpers import create_dummy_user


class TestCreatePost(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user()
        self.url = reverse('posts')
        
        self.client.force_authenticate(self.user)
    
    def test_create_post(self):
        payload = {
            'content': 'Olá, mundo!'
        }
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, json.dumps(response.data, indent=4))