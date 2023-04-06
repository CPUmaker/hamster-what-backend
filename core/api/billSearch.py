from rest_framework import generics
from core.models.bill import Bill, BillSearchQuerySet
from core.serializers.bill import BillSerializer
from rest_framework import permissions, authentication

from datetime import date, datetime


class SearchBillListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # item = categories  ----->    keyword = 1/2/3/4/5 ..
    #        price       ----->    keyword = price
    #        date        ----->    keyword = month / day / year    ----->  date: yyyy/mm/dd
    #        title       ----->    keyword = title

    def get_queryset(self, *args, **kwargs):
        qs = BillSearchQuerySet(Bill)
        item = self.request.query_params.get("item")
        result = Bill.objects.none()
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        keyword = self.request.query_params.get("keyword")
        
        if item == "categories":
            result = qs.searchCategories(keyword, user=user)
        elif item == "price":
            result = qs.searchPrice(keyword, user=user)
        elif item == "date":
            anchor_date = self.request.query_params.get("date", None)
            anchor_date = date.today() if anchor_date is None else datetime.strptime(anchor_date, '%Y-%m-%d')
            if keyword == "year":
                result = qs.searchByYear(user=user, anchor_date=anchor_date)
            elif keyword == "month":
                result = qs.searchByMonth(user=user, anchor_date=anchor_date)
            elif keyword == "day":
                result = qs.searchByDay(user=user, anchor_date=anchor_date)
        elif item == "title":
            result = qs.searchTitle(keyword, user=user)
        return result