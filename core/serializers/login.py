from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        usersByEmail = User.objects.filter(email=data['username'].lower())
        if len(usersByEmail) != 0:
            username = usersByEmail[0].username
            data['username'] = username

        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Invalid Credentials.')
        if not user.is_active:
            raise serializers.ValidationError('Account is not activated.')
        return user
        
