from rest_framework import serializers

from core.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'birthday', 'country', 'city', 'affiliation', 'photo')
