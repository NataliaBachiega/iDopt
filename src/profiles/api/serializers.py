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
