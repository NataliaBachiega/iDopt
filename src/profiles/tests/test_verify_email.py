from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from profiles.models import VerificationCode


class TestVerifyEmail(APITestCase):
    def test_can_user_get_verification_code(self):
        '''Verifica se o usuário consegue gerar um código de verificação para o cadastro no
        sistema
        '''

        url = reverse('verify-email')
        email = 'emailfeliz@idopt.com'

        response = self.client.get(f'{url}?email={email}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            VerificationCode.objects.filter(email=email).count(),
            1,
            'O código de verification não foi criado.'
        )
        
    def test_can_user_verify_email(self):
        '''Verifica se o usuário consegue verificar o email.'''
        
        url = reverse('verify-email')
        email = 'emailfeliz@idopt.com'
        code_recv_from_email = '123456'
        
        VerificationCode.objects.create(
            code=code_recv_from_email,
            email=email,
            enabled=False
        )
        
        response = self.client.post(url, data={'email': email, 'code': code_recv_from_email})
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        verification_code = VerificationCode.objects.get(email=email, code=code_recv_from_email)
        
        self.assertTrue(verification_code.enabled, 'O código de verificação não foi ativado.')