from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Invalid Credentials.')
        if not user.is_active:
            raise serializers.ValidationError('Account is not activated.')
        return user
        
