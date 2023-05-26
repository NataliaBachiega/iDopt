import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from idopt.helpers import create_dummy_post, create_dummy_user
from posts.models import Post


class TestRetrieveDeletePost(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user()

        self.client.force_authenticate(self.user)
        self.post = create_dummy_post(self.user)
    

    def test_retrieve_post(self):
        post_id = Post.objects.first().id
        url = reverse('post-detail', kwargs={'pk': post_id})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.dumps(response.data, indent=4))
        self.assertEqual(response.data['id'], self.post.id, 'Post errado foi retornado!!!!')
    

    def test_delete_post(self):
        '''
        Verifica se um usuário com permissão pode apagar um post.
        '''
        url = reverse('post-detail', kwargs={'pk': self.post.id})

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, json.dumps(response.data, indent=4))
        self.assertEqual(Post.objects.count(), 0, 'Post não foi apagado!!!!')
    
    def test_delete_someones_else_post(self):
        someone_else = create_dummy_user()
        other_post = create_dummy_post(someone_else)

        post_id = other_post.id
        url = reverse('post-detail', kwargs={'pk': post_id})

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, json.dumps(response.data, indent=4))
        self.assertEqual(Post.objects.count(), 2, 'Post não deveria ter sido apagado!!!!')
