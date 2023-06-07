import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from idopt.helpers import create_dummy_post, create_dummy_user
from posts.models import Post


class TestListComment(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user()
        self.client.force_authenticate(self.user)

        self.post = create_dummy_post(self.user)
        self.url = reverse('post-comments', kwargs={'pk': self.post.id})

        for _ in range(5):
            create_dummy_post(self.user, comment_of=self.post)
    
    def test_get_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.dumps(response.data, indent=4))
        self.assertIsInstance(response.data['results'], list)

        originalPost = Post.objects.get(id=self.post.id)

        # Garante que apenas os posts corretos (comentário) foi enviado.
        self.assertEqual(len(response.data['results']), originalPost.comments.count())