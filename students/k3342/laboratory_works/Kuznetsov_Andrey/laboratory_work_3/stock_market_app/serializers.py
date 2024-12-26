from rest_framework import serializers
from .models import Agency, Broker, Producer, Product, Batch, BatchProduct, Client, ClientPurchase, Transaction
from django.db.models import Sum


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'


class BrokerSerializer(serializers.ModelSerializer):
    agency = AgencySerializer()

    class Meta:
        model = Broker
        fields = '__all__'


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class BatchProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    batch = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())  # Only batch ID for simplicity

    class Meta:
        model = BatchProduct
        fields = ['product', 'batch', 'quantity', 'price_per_unit']


class BatchSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer()
    batch_products = BatchProductSerializer(many=True)  # Nested BatchProduct serializer for each batch

    class Meta:
        model = Batch
        fields = '__all__'


class ClientPurchaseSerializer(serializers.ModelSerializer):
    batch = BatchSerializer()

    class Meta:
        model = ClientPurchase
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    batch = BatchSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class ProductRevenueSerializer(serializers.ModelSerializer):
    total_revenue = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'total_revenue']

    def get_total_revenue(self, obj):
        """
        Calculate the total revenue for a product.
        """
        total_revenue = BatchProduct.objects.filter(product=obj).annotate(
            revenue=Sum('quantity' * 'price_per_unit')
        ).aggregate(Sum('revenue'))['revenue__sum'] or 0
        return total_revenue


class ClientLoyaltySerializer(serializers.ModelSerializer):
    total_purchases = serializers.IntegerField(source='purchases.count')
    total_spent = serializers.DecimalField(
        source='purchases.aggregate(Sum("total_price"))', max_digits=10, decimal_places=2
    )

    class Meta:
        model = Client
        fields = ['id', 'name', 'total_purchases', 'total_spent']
