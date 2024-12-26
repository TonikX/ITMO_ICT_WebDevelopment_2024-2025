from datetime import datetime

from django.db import connection
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, get_object_or_404, \
    RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Agency, BrokerCompany, Broker, BrokerInfo, Manufacturer, Product, ProductGroup, Order, BatchProduct
from .permissions import IsBroker
from .queries import get_user_month_transaction_sum
from .serializers import AgencyDetailSerializer, AgencyCreateSerializer, AgencySerializer, \
    BrokerCompanyListSerializer, BrokerCompanyDetailSerializer, CreateBrokerSerializer, ManufacturerDetailSerializer, \
    ManufacturerCreateSerializer, ManufacturerListSerializer, CreateProductSerializer, CreateOrderSerializer, \
    OrderSerializer
from .serializers import ProductSerializer


class index(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'message': 'Hello, World!',
            'authenticated?': request.user.is_authenticated,
            'staff?': request.user.is_staff,
        }, status=200)


class ManageStateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "This page is for managing state on the app without touching admin panel GUI",
        })


class AgencyList(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    paginate_by = 10

    def get_queryset(self):
        return Agency.objects.filter(manager=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return AgencySerializer
        return AgencyCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(manager=self.request.user)
        return Response(serializer.data, status=201)


class AgencyDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AgencyDetailSerializer

    def get_object(self):
        agency = Agency.objects.get(id=self.kwargs['pk'])
        if agency.manager != self.request.user:
            raise PermissionDenied({"You cannot access this Agency"})
        return agency


class CreateBrokerCompany(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BrokerCompanyListSerializer

    def create(self, request, *args, **kwargs):
        obj = get_object_or_404(Agency, id=self.kwargs['pk'])
        if obj.manager != self.request.user:
            raise PermissionDenied({"You cannot access this Agency"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(agency=obj)
        return Response(serializer.data, status=201)


class BrokerCompanyDetails(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BrokerCompanyDetailSerializer

    def get_object(self):
        broker_company = get_object_or_404(BrokerCompany, id=self.kwargs['pk'])
        if broker_company.agency.manager != self.request.user:
            raise PermissionDenied({"You cannot access this Broker Company"})
        return broker_company

    def get_serializer_class(self, *args, **kwargs):
        return BrokerCompanyDetailSerializer


class AddBroker(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateBrokerSerializer

    def create(self, request, *args, **kwargs):
        company = get_object_or_404(BrokerCompany, id=self.kwargs['pk'])
        candidate = get_object_or_404(Broker, id=request.data['broker_id'])

        if hasattr(candidate, 'brokerinfo'):
            raise PermissionDenied({"You cannot access this Broker"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        BrokerInfo.objects.create(broker_company=company,
                                  broker=candidate,
                                  monthly_fee=request.data['monthly_fee'],
                                  contact_number=request.data['contact_number'], )

        return Response(serializer.data, status=201)


class ManufacturerList(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    paginate_by = 10
    serializer_class = ManufacturerCreateSerializer

    def get_queryset(self):
        return Manufacturer.objects.filter(manager=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return ManufacturerListSerializer

        return ManufacturerCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(manager=self.request.user)
        return Response(serializer.data, status=201)


class ManufacturerDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ManufacturerDetailSerializer

    def get_object(self):
        manufacturer = get_object_or_404(Manufacturer, id=self.kwargs['pk'])
        if manufacturer.manager != self.request.user:
            raise PermissionDenied({"You cannot access this Manufacturer"})
        return manufacturer


class CreateProduct(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateProductSerializer

    def create(self, request, *args, **kwargs):
        manufacturer = get_object_or_404(Manufacturer, id=self.kwargs['pk'])
        if manufacturer.manager != self.request.user:
            raise PermissionDenied({"You cannot access this Manufacturer"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_group, _ = ProductGroup.objects.get_or_create(group=serializer.data['product_group_name'])

        Product.objects.create(
            name=serializer.data['name'],
            manufacturer=manufacturer,
            quantity=request.data['quantity'],
            production_date=request.data['production_date'],
            expiry_period=request.data['expiry_period'],
            product_group=product_group

        )

        return Response(serializer.data, status=201)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(quantity__gt=0)
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.filter(quantity__gt=0)
    serializer_class = ProductSerializer


class OrderProduct(CreateAPIView):
    permission_classes = [IsBroker]
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'brokerinfo'):
            raise PermissionDenied({"You cannot create orders"})
        current_order = Order.objects.filter(status='op', broker=request.user)

        if current_order.exists():
            current_order = current_order.first()
        else:
            current_order = Order.objects.create(broker=request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if BatchProduct.objects.filter(product_id=self.kwargs['pk'], batch=current_order, ).exists():
            raise PermissionDenied({"You already have an order. If you want to change it, do it in the proper place"})
        BatchProduct.objects.create(product_id=self.kwargs['pk'], batch=current_order, **serializer.data)
        return Response(serializer.data, status=201)


class BrokerList(ListAPIView):
    permission_classes = [IsBroker]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(broker=self.request.user)


class OrderDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsBroker]
    serializer_class = OrderSerializer

    def get_object(self):
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        if order.broker != self.request.user:
            raise PermissionDenied({"You cannot access this order"})
        return order


class ApproveOrder(APIView):
    permission_classes = [IsBroker]

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        if order.broker != self.request.user:
            raise PermissionDenied({"You cannot access this order"})

        if order.status != 'op':
            raise PermissionDenied({"You cannot approve this order, It is already approved"})

        order.status = 'ap'
        order.save()
        return Response({'status': 'Approved'})


class BrokerStatistics(APIView):
    permission_classes = [IsBroker]

    def get(self, request, *args, **kwargs):
        filter_month = request.GET.get('month', datetime.today().month)
        user_id = request.user.id

        sql = get_user_month_transaction_sum(user=user_id, month=filter_month)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return Response({'Your monthly stats': {
            'bought': rows[0][0],
            'paid': rows[0][1],
        }})
