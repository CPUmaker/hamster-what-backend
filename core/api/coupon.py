from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.serializers.coupon import CouponSerializer
from core.models.coupon import Coupon


class CouponViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
