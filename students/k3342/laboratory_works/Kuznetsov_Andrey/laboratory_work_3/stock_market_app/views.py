from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import models
from django.db.models import Sum, Max, Count, Q
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404


from .models import Agency, Broker, Producer, Product, Batch, BatchProduct, Client, ClientPurchase, Transaction
from .serializers import (
    AgencySerializer, BrokerSerializer, ProducerSerializer,
    ProductSerializer, BatchSerializer, BatchProductSerializer,
    ClientLoyaltySerializer, ClientPurchaseSerializer, TransactionSerializer,
    ProductRevenueSerializer
)


class ParentDeleteProtectedMixin:
    """
    Controls parent/children object deletion and bans cascade removing.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        related_models = []

        if isinstance(instance, Agency):
            related_models = ['brokers']
        elif isinstance(instance, Broker):
            related_models = ['batches']
        elif isinstance(instance, Producer):
            related_models = ['products']
        elif isinstance(instance, Product):
            related_models = ['batch_products']
        elif isinstance(instance, Batch):
            related_models = ['batch_products', 'purchases', 'transactions']
        elif isinstance(instance, Client):
            related_models = ['purchases']

        for related_model in related_models:
            if getattr(instance, related_model).exists():
                return Response(
                    {
                        "error": f"Impossible to delete an object, because it has children elements in {related_model}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().destroy(request, *args, **kwargs)


class AgencyViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class BrokerViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer

    @swagger_auto_schema(
        operation_description="Delete the broker by name.",
        responses={200: BrokerSerializer},
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY,
                description="Broker name.",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    @action(detail=False, methods=['delete'], url_path='delete-by-name')
    def delete_by_name(self, request):
        """
        Delete a broker by name.
        """
        name = request.query_params.get('name')

        if not name:
            return Response({'error': 'Please provide the name of the broker to delete.'},
                            status=status.HTTP_400_BAD_REQUEST)

        broker = get_object_or_404(Broker, name=name)
        broker.delete()
        return Response({'message': f'Broker {name} has been deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Get the broker by name or agency.",
        responses={200: BrokerSerializer},
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY,
                description="Broker name.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'address', openapi.IN_QUERY,
                description="Producer agency address.",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='by-criteria')
    def get_by_criteria(self, request):
        name = request.query_params.get('name')
        address = request.query_params.get('address')

        queryset = Broker.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if address:
            queryset = queryset.filter(agency__address__icontains=address)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProducerViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

    @swagger_auto_schema(
        operation_description="Get the producer by name.",
        responses={200: ProducerSerializer},
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY,
                description="Producer name.",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    @action(detail=False, methods=['get'], url_path='by-name')
    def get_by_name(self, request):
        """
        Get a producer by name.
        """
        name = request.query_params.get('name')

        if not name:
            return Response({'error': 'Please provide the name of the producer.'}, status=status.HTTP_400_BAD_REQUEST)

        producer = get_object_or_404(Producer, name=name)
        serializer = self.get_serializer(producer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Find the producer with the highest revenue for the given period.",
        responses={200: ProducerSerializer},
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date of the period.",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date of the period.",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def top_producer_by_revenue(self, request):
        """
        Find the producer with the highest revenue for the given period.
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({'error': 'Please provide both start_date and end_date.'},
                            status=status.HTTP_400_BAD_REQUEST)

        top_producer = Producer.objects.filter(
            products__batch_products__batch__contract_date__range=(start_date, end_date)
        ).annotate(
            total_revenue=Sum(
                models.F('products__batch_products__quantity') *
                models.F('products__batch_products__price_per_unit')
            )
        ).order_by('-total_revenue').values('name', 'total_revenue').first()

        return Response(top_producer if top_producer else {'message': 'No data available for the specified period.'})


class ProductViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="Get the list of products that have never been sold.",
        responses={200: ProductRevenueSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def never_sold_products(self, request):
        """
        Get the list of products that have never been sold.
        """
        unsold_products = Product.objects.filter(batch_products__isnull=True).values('id', 'name', 'producer__name')
        return Response(unsold_products)

    @swagger_auto_schema(
        operation_description="Get the latest batch information for each product.",
        responses={200: ProductRevenueSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def latest_batches(self, request):
        """
        Get the latest batch information for each product.
        """
        latest_batches = Product.objects.annotate(
            latest_batch_id=Max('batch_products__batch__id')
        ).filter(
            latest_batch_id__isnull=False
        ).values(
            'id', 'name', 'latest_batch_id',
            'batch_products__batch__shipment_date',
            'batch_products__batch__broker__name',
            'batch_products__price_per_unit',
            'batch_products__quantity'
        )

        return Response(latest_batches)


class BatchViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


class BatchProductViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = BatchProduct.objects.all()
    serializer_class = BatchProductSerializer

    @swagger_auto_schema(
        operation_description="Get all batches with expired products.",
        responses={200: BatchProductSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def expired_products(self, request):
        """
        Get all batches with expired products.
        """
        expired_batches = Batch.objects.filter(
            batch_products__product__expiration_date__lt=models.F('shipment_date')
        ).distinct().values(
            'id', 'supply_conditions', 'contract_date', 'shipment_date',
            'broker__name', 'batch_products__product__name'
        )

        return Response(expired_batches)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientLoyaltySerializer

    @swagger_auto_schema(
        operation_description="Find clients who only purchased products from a specific broker.",
        responses={200: ClientLoyaltySerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'broker_id', openapi.IN_QUERY,
                description="Broker ID",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def loyal_clients(self, request):
        """
        Find clients who have only purchased products from a specific broker.
        """
        broker_id = request.query_params.get('broker_id')

        if not broker_id:
            return Response({'error': 'Please provide broker_id as a query parameter.'},
                            status=status.HTTP_400_BAD_REQUEST)

        loyal_clients = Client.objects.annotate(
            brokers_count=Count('purchases__batch__broker', distinct=True),  # Считаем количество разных брокеров
            target_broker_count=Count('purchases__batch__broker', filter=Q(purchases__batch__broker__id=broker_id))
        ).values('id', 'name', 'address', 'brokers_count', 'target_broker_count')

        return Response(loyal_clients)

class ClientPurchaseViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = ClientPurchase.objects.all()
    serializer_class = ClientPurchaseSerializer


class TransactionViewSet(ParentDeleteProtectedMixin, viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
