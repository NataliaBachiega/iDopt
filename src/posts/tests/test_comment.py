import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from idopt.helpers import create_dummy_post, create_dummy_user
from posts.models import Post

class TestComment(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user()
        self.client.force_authenticate(self.user)
        self.post = create_dummy_post(self.user)
    
    def test_can_create_comment(self):
        url = reverse('posts')
        payload = {
            'comment_of': self.post.id,
            'content': 'Olá, mundo!'
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, json.dumps(response.data, indent=4))

        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.comments.count(), 1)
        self.assertIsInstance(response.data['comment_of'], int)