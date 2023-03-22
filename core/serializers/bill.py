from rest_framework import serializers
from core.models.bill import Bill
from rest_framework.reverse import reverse
from core.serializers.OwnerSerializers import UserSerializer


class BillSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Bill
        fields = (
            'user',
            'url',
            'wallet',
            'date',
            'datetime',
            'price',
            'categories',
            'comment'
        )
    
    def get_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        return reverse("bill-detail", kwargs = {"pk": obj.pk}, request = request)