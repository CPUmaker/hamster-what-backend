from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.serializers.coupon import CouponSerializer
from core.models.coupon import Coupon


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
