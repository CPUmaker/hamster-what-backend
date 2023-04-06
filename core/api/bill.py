from rest_framework import generics, mixins, status
from core.models.bill import Bill
from core.serializers.bill import BillSerializer
from rest_framework.response import Response
from rest_framework import permissions, authentication


class BillListCreate(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     authentication.TokenAuthentication
    # ]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        default_user = self.request.user
        if not default_user:
            default_user = None
        serializer.is_valid()
        serializer.save(user = default_user)

    def get_queryset(self, *args, **kwargs):
        qs =super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return Bill.objects.none()
        return qs.filter(user = user)
    


bill_list_create_api = BillListCreate.as_view()


class BillDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        default_user = self.request.user
        if not default_user:
            default_user = None
        serializer.save(user = default_user)

    def get_queryset(self, *args, **kwargs):
        qs =super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return Bill.objects.none()
        return qs.filter(user = user)

bill_detail_api = BillDetail.as_view()
