from rest_framework import generics
from core.models.bill import Bill, BillSearchQuerySet
from core.serializers.bill import BillSerializer
from rest_framework import permissions, authentication

class SearchBillListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # item = categories  ----->    keyword = 1/2/3/4/5 ..
    #        price       ----->    keyword = price
    #        date        ----->    keyword = month / day
    #        title       ----->    keyword = title

    def get_queryset(self, *args, **kwargs):
        print(self.request.query_params)
        qs = BillSearchQuerySet(Bill)
        item = self.request.GET.get("item")
        result = Bill.objects.none()
        user = None
        if self.request.user.is_authenticated:
            user =  self.request.user
        keyword = self.request.GET.get("keyword")
        if item == "categories":
            result = qs.searchCategories(keyword, user=user)
        elif item == "price":
            result = qs.searchPrice(keyword, user=user)
        elif item == "date":
            if keyword == "month":
                result = qs.searchThisMonth(user=user)
            elif keyword == "today":
                result = qs.searchToday(user=user)
        elif item == "title":
            result = qs.searchTitle(keyword, user=user)
        return result