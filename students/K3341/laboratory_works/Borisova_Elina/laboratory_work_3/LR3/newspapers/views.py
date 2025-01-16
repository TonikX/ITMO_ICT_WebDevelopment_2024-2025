from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Editor, Newspaper, PrintShop, PostOffice, PrintRun, Delivery
from .serializers import (
    EditorSerializer,
    NewspaperSerializer,
    PrintShopSerializer,
    PostOfficeSerializer,
    PrintRunSerializer,
    DeliverySerializer,
)


class EditorViewSet(viewsets.ModelViewSet):
    queryset = Editor.objects.all()
    serializer_class = EditorSerializer
    permission_classes = [IsAuthenticated]


class NewspaperViewSet(viewsets.ModelViewSet):
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'index']

    @action(detail=True, methods=['get'])
    def index_and_price(self, request, pk=None):
        newspaper = self.get_object()
        data = {
            'index': newspaper.index,
            'price': newspaper.price,
        }
        return Response(data)


class PrintShopViewSet(viewsets.ModelViewSet):
    queryset = PrintShop.objects.all()
    serializer_class = PrintShopSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        printshop = self.get_object()
        print_runs = PrintRun.objects.filter(printshop=printshop)

        total_newspapers = print_runs.aggregate(total=Sum('quantity'))['total'] or 0
        newspapers = print_runs.values('newspaper__name').annotate(total=Sum('quantity'))
        deliveries = Delivery.objects.filter(printshop=printshop).values(
            'post_office__number', 'newspaper__name'
        ).annotate(total=Sum('quantity'))

        data = {
            'printshop': printshop.name,
            'total_newspapers': total_newspapers,
            'newspapers': list(newspapers),
            'deliveries': list(deliveries),
        }
        return Response(data)


class PostOfficeViewSet(viewsets.ModelViewSet):
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['number', 'address']


class PrintRunViewSet(viewsets.ModelViewSet):
    queryset = PrintRun.objects.all()
    serializer_class = PrintRunSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'newspaper_id',
                openapi.IN_QUERY,
                description="ID газеты",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def total_prints_for_newspaper(self, request):
        newspaper_id = request.query_params.get('newspaper_id')
        if not newspaper_id:
            return Response({'error': 'Параметр newspaper_id обязателен.'}, status=400)
        try:
            total = PrintRun.objects.filter(newspaper_id=newspaper_id).aggregate(Sum('quantity'))['quantity__sum']
            return Response({'total_prints': total or 0})
        except ValueError:
            return Response({'error': 'Некорректное значение newspaper_id.'}, status=400)


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'price',
                openapi.IN_QUERY,
                description="Цена",
                type=openapi.TYPE_NUMBER,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def post_offices_receiving_expensive_newspapers(self, request):
        price = request.query_params.get('price')
        if not price:
            return Response({'error': 'Параметр price обязателен.'}, status=400)
        try:
            price = float(price)
            deliveries = Delivery.objects.filter(
                print_run__newspaper__price__gt=price
            ).select_related('post_office')
            addresses = deliveries.values_list('post_office__address', flat=True).distinct()
            return Response({'addresses': addresses})
        except ValueError:
            return Response({'error': 'Некорректное значение цены.'}, status=400)

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'quantity',
                openapi.IN_QUERY,
                description="Количество",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def newspapers_with_low_circulation(self, request):
        quantity = request.query_params.get('quantity')
        if not quantity:
            return Response({'error': 'Параметр quantity обязателен.'}, status=400)
        try:
            quantity = int(quantity)
            deliveries = Delivery.objects.filter(quantity__lt=quantity).select_related('print_run__newspaper', 'post_office')
            results = deliveries.values(
                'print_run__newspaper__name', 'post_office__number', 'quantity'
            )
            return Response({'results': list(results)})
        except ValueError:
            return Response({'error': 'Некорректное значение количества.'}, status=400)

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'newspaper_name',
                openapi.IN_QUERY,
                description="Название газеты",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'printshop_id',
                openapi.IN_QUERY,
                description="ID типографии",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def newspaper_distribution(self, request):
        newspaper_name = request.query_params.get('newspaper_name')
        printshop_id = request.query_params.get('printshop_id')
        if not newspaper_name or not printshop_id:
            return Response({'error': 'Параметры обязательны: newspaper_name и printshop_id.'}, status=400)
        deliveries = Delivery.objects.filter(
            print_run__newspaper__name=newspaper_name,
            printshop_id=printshop_id
        ).select_related('post_office')
        results = deliveries.values(
            'post_office__number', 'post_office__address', 'quantity'
        )
        return Response({'results': list(results)})