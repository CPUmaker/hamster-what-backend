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
            2: "Groceries",
            3: "Transportation",
            4: "clothing",
            5: "Entertainment",
            6: "Bill",
            7: "Sports",
            8: "Electronics",
            9: "Travel",
            10: "House & Car",
            11: "Salary",
            12: "Others"
        }
        queryset = self.filter_queryset(self.get_queryset())
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        data = {}

        for i in range(1,12):
            qs = BillSearchQuerySet(Bill).searchCategories(query=i, user=user)
            if item == 'today':
                qs = qs.searchToday(user=user)
            elif item == 'month':
                qs = qs.searchThisMonth(user=user)
            total_price = qs.aggregate(Sum('price'))
            data[categorieModel[i]] = total_price['price__sum']
        return response.Response(data)
    
BillSumPriceListViewAPI = BillSumPriceListView.as_view()