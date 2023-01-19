from rest_framework import serializers

from core.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'birthday', 'country', 'city', 'affiliation', 'photo')
