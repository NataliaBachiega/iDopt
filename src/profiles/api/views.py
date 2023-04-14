import random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from profiles.api.serializers import DeviceSerializer, GetVerificationCodeSerializer, RegistrationSerializer, UserSerializer, VerifyEmailSerializer
from profiles.models import Device, IdoptUser, VerificationCode
from rest_framework.generics import CreateAPIView


class VerifyEmail(APIView):
    def get(self, request: Request) -> Response:
        serializer = GetVerificationCodeSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Gera um código de verificação.
        valid = False
        code = None
        while not valid:
            # Gera um código aleatório com 6 dígitos
            code = str(random.randrange(0, 10**6)).zfill(6)

            if not VerificationCode.objects.filter(code=code).exists():
                valid = True

        VerificationCode.objects.create(
            code=code,
            email=serializer.data.get('email')
        )

        # send_mail()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request) -> Response:
        serializer = VerifyEmailSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            verification_code = VerificationCode.objects.get(
                email=serializer.data.get('email'),
                code=serializer.data.get('code'),
            )
            
            # TODO Verificar se o código existe há muito tempo.
            
            verification_code.enabled = True
            verification_code.save()
            
        except VerificationCode.DoesNotExist:
            return Response(
                {'email': 'Código de verificação inválido.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class Registration(APIView):
    def post(self, request: Request) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verifica se o usuário verificou seu email
        user_data = serializer.data.get('user')
        valid: bool = False
        
        try:
            verification_code = VerificationCode.objects.get(
                email=user_data.get('email'),
                enabled=True
            )
            
            # Ok, o usuário verificou seu email. Podemos apagar o código agora.
            verification_code.delete()
            valid = True
            
        except VerificationCode.DoesNotExist:
            pass
        
        if not valid:
            return Response(data={'email': 'Email não verificado.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Cria o usuário.
        user = IdoptUser(**user_data)
        user.set_password(user_data.get('password'))
        user.save()
        
        # Cria o dispositivo.
        device_data = serializer.data.get('device')
        device = Device(**device_data, owner=user)
        device.save()
        
        # Retorna a resposta.
        return Response(
            data={
                'user': UserSerializer(user).data,
                'device': DeviceSerializer(device).data,
                'token': 'TODO',
            },
            status=status.HTTP_201_CREATED,
        )