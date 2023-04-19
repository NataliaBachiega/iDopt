from faker import Faker
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from profiles.models import Device, IdoptUser, VerificationCode


class TestRegistration(APITestCase):
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

        response = self.client.post(
            url, data={'email': email, 'code': code_recv_from_email})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        verification_code = VerificationCode.objects.get(
            email=email, code=code_recv_from_email)

        self.assertTrue(verification_code.enabled,
                        'O código de verificação não foi ativado.')

    def test_registration(self):
        '''
        Verifica o endpoint de cadastro
        '''

        # Primeiro, criamos um código de verificação válido na base.
        user_email = 'emailfeliz@idopt.com'

        VerificationCode.objects.create(
            code='123456',
            email=user_email,
            enabled=True,
        )

        url = reverse('register')
        faker = Faker()

        payload = {
            'user': {
                'email': user_email,
                'username': faker.user_name(),
                'password': faker.password(),
            },
            'device': {
                'os': 'android',
                'os_version': '10',
                'fcm_token': 'token',
                'name': 'Galaxy S23'
            }
        }

        # Envia a requisição
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, msg=response.data)

        # Verifica se a resposta possui informações corretas
        self.assertIsInstance(response.data['user'], dict)
        self.assertIsInstance(response.data['device'], dict)
        self.assertIsInstance(response.data['token'], str)

        # Verifica se as instancias foram criadas na base de dados.
        self.assertEqual(IdoptUser.objects.count(), 1)
        self.assertEqual(Device.objects.count(), 1)

    def test_registration_without_verification_code(self):
        '''
        Verifica se a API consegue lidar com um usuário que não verificou seu email
        '''

        # Não há nenhum código de verificação na base de dados. Vamos direto para o cadastro.
        url = reverse('register')
        faker = Faker()

        payload = {
            'user': {
                'email': faker.email(),
                'username': faker.user_name(),
                'password': faker.password(),
            },
            'device': {
                'os': 'android',
                'os_version': '10',
                'fcm_token': 'token',
                'name': 'Galaxy S23'
            }
        }

        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN, msg=response.data)

        # Verifica se a base de dados segue sem nenhum usuário.
        self.assertEqual(IdoptUser.objects.count(), 0)
        self.assertEqual(Device.objects.count(), 0)
