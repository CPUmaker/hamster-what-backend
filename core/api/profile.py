from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.serializers.profile import ProfileSerializer


class ProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
