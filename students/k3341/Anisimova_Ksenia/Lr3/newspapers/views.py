from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Editor, Newspaper, PrintShop, PostOffice, Distribution
from .serializers import (
    EditorSerializer,
    NewspaperSerializer,
    PrintShopSerializer,
    PostOfficeSerializer,
    DistributionSerializer,
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
            'price_updated_at': newspaper.price_updated_at,
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
        distributions = Distribution.objects.filter(printshop=printshop)

        total_newspapers = distributions.aggregate(total=Sum('copies_printed'))['total'] or 0
        newspapers = distributions.values('newspaper__name').annotate(total=Sum('copies_printed'))
        post_office_distributions = distributions.values(
            'postoffice__office_number', 'newspaper__name'
        ).annotate(total=Sum('copies_sent'))

        data = {
            'printshop': printshop.name,
            'total_newspapers': total_newspapers,
            'newspapers': list(newspapers),
            'post_office_distributions': list(post_office_distributions),
        }
        return Response(data)


class PostOfficeViewSet(viewsets.ModelViewSet):
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['office_number', 'address']


class DistributionViewSet(viewsets.ModelViewSet):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'newspaper_name',
                openapi.IN_QUERY,
                description="Название газеты",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def newspapers_printed_at_address(self, request):
        newspaper_name = request.query_params.get('newspaper_name')
        if not newspaper_name:
            return Response({'error': 'Параметр newspaper_name обязателен.'}, status=400)
        distributions = Distribution.objects.filter(
            newspaper__name=newspaper_name
        ).select_related('printshop')
        addresses = distributions.values_list('printshop__address', flat=True).distinct()
        return Response({'addresses': addresses})

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'printshop_id',
                openapi.IN_QUERY,
                description="Printshop Id",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def editor_with_largest_circulation(self, request):
        printshop_id = request.query_params.get('printshop_id')
        if not printshop_id:
            return Response({'error': 'Параметр printshop_id обязателен.'}, status=400)
        try:
            distributions = Distribution.objects.filter(
                printshop_id=printshop_id
            ).select_related('newspaper__editor')
            largest_distribution = distributions.order_by('-copies_printed').first()
            if largest_distribution:
                editor = largest_distribution.newspaper.editor
                surname = editor.name.split()[0]  # Предполагается, что фамилия первая
                return Response({'editor_surname': surname})
            else:
                return Response({'error': 'Нет данных для указанной типографии.'}, status=404)
        except PrintShop.DoesNotExist:
            return Response({'error': 'Типография не найдена.'}, status=404)

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
            distributions = Distribution.objects.filter(
                newspaper__price__gt=price
            ).select_related('postoffice')
            addresses = distributions.values_list('postoffice__address', flat=True).distinct()
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
            distributions = Distribution.objects.filter(
                copies_sent__lt=quantity
            ).select_related('newspaper', 'postoffice')
            results = distributions.values(
                'newspaper__name', 'postoffice__office_number', 'copies_sent'
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
                'printshop_address',
                openapi.IN_QUERY,
                description="Адрес производства",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def newspaper_distribution_at_address(self, request):
        newspaper_name = request.query_params.get('newspaper_name')
        printshop_address = request.query_params.get('printshop_address')
        if not newspaper_name or not printshop_address:
            return Response({
                'error': 'Параметры newspaper_name и printshop_address обязательны.'
            }, status=400)
        distributions = Distribution.objects.filter(
            newspaper__name=newspaper_name,
            printshop__address=printshop_address
        ).select_related('postoffice')
        post_offices = distributions.values(
            'postoffice__office_number', 'postoffice__address'
        ).distinct()
        return Response({'post_offices': list(post_offices)})
