from rest_framework import serializers

from profiles.models import Device, IdoptUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdoptUser
        exclude = ['password']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class GetVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''
    Serializador usado no cadastro do usuário. Parte do [RegistrationSerializer].
    '''
    class Meta:
        model = IdoptUser
        fields = ['username', 'password', 'email']


class DeviceRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'os', 'os_version', 'fcm_token']


class RegistrationSerializer(serializers.Serializer):
    user = UserRegistrationSerializer()
    device = DeviceRegistrationSerializer()

class LoginSerializer(serializers.Serializer):
    '''
    Este serializador valida os dados de login do usuário.
    Os dados de dispositivo são necessários para podermos enviar notificações no futuro.
    '''
    
    username = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(required=True)
    device = DeviceRegistrationSerializer(required=True)
    
    def validate(self, attrs):
        try:
            user = IdoptUser.objects.get(username=attrs.get('username'))
            
            if not user.check_password(attrs.get('password')):
                raise serializers.ValidationError({'password': 'Senha incorreta.'})
        except IdoptUser.DoesNotExist:
            raise serializers.ValidationError({'username': 'Usuário não encontrado.'})
        
        # Retornar os atributos significa que a validação foi bem sucedida.
        # Quem define isso é o Django, não eu 🙂.
        return attrs