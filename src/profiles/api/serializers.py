from rest_framework import serializers


class GetVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)