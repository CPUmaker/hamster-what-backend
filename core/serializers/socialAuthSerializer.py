from rest_framework import serializers


class AppleUserInputSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True, allow_blank=False)


class GoogleUserInputSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True, allow_blank=False)


class FacebookUserInputSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True, allow_blank=False)
