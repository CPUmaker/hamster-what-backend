from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth.models import User

from core.models.profile import Profile

class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        if 'username' in data and User.objects.filter(username=data['username']).count() != 0:
            raise serializers.ValidationError({
                'username': "This username is being used by others."
            })
        if 'email' in data and User.objects.filter(username=data['email']).count() != 0:
            raise serializers.ValidationError({
                'email': "This email address is being used by others."
            })
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('email', None):
            instance.is_active = False
        instance.save()
        return instance


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = UserUpdateSerializer(required=False)

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'birthday', 'country', 'city', 'affiliation', 'photo')

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        if user_data:
            user = instance.user
            user_serializer = UserUpdateSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.update(user, user_data)
        
        for attr in self.Meta.fields:
            if attr == 'user':
                continue
            setattr(instance, attr, validated_data.get(attr, getattr(instance, attr)))
        instance.save()
        return instance
