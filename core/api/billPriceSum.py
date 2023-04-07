from rest_framework import generics, response
from core.models.bill import Bill, BillSearchQuerySet
from core.serializers.bill import BillSerializer
from rest_framework import permissions, authentication
from django.db.models import Sum

class BillSumPriceListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
    def get(self, request, *args, **kwargs):
        item = request.GET.get('item')

        categorieModel = {
            1: "Food",
            2: "Transportation",
            3: "Shopping",
            4: "Entertainment",
            5: "Housing",
            6: "Utilities",
            7: "Other",
            8: "Salary",
            9: "Interest",
            10: "Investment",
            11: "Child benefit",
            12: "Pension",
            13: "Income",
        }
        queryset = self.filter_queryset(self.get_queryset())
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        data = {}

        for i in range(1,12):
            qs = BillSearchQuerySet(Bill).searchCategories(query=i, user=user)
            if item == 'today':
                qs = qs.searchByDay(user=user)
            elif item == 'month':
                qs = qs.searchByMonth(user=user)
            total_price = qs.aggregate(Sum('price'))
            data[categorieModel[i]] = total_price['price__sum']
        return response.Response(data)
    
BillSumPriceListViewAPI = BillSumPriceListView.as_view()