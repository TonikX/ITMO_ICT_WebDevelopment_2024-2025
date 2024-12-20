from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Agency, BrokerCompany, Broker, Manufacturer, Product, BatchProduct, Order


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class BrokerSerializer(ModelSerializer):
    monthly_fee = serializers.SerializerMethodField()
    contact_number = serializers.SerializerMethodField()

    class Meta:
        model = Broker
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'monthly_fee',
                  'contact_number']

    def get_monthly_fee(self, obj):
        return obj.brokerinfo.monthly_fee

    def get_contact_number(self, obj):
        return obj.brokerinfo.contact_number


class BrokerCompanyListSerializer(ModelSerializer):
    class Meta:
        model = BrokerCompany
        fields = ['id', 'monthly_fee', 'contact_number']


class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', 'name', 'contact_number', 'country']


class AgencyDetailSerializer(ModelSerializer):
    manager = CustomUserSerializer(read_only=True)
    broker_companies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Agency
        fields = [
            'id',
            'name',
            'country',
            'contact_number',
            'address',
            'legal_address',
            'manager',
            'broker_companies'
        ]

    def get_broker_companies(self, obj):
        broker_agencies = BrokerCompany.objects.filter(agency=obj)
        return BrokerCompanyListSerializer(broker_agencies, many=True).data


class AgencyCreateSerializer(ModelSerializer):
    class Meta:
        model = Agency
        fields = ['name',
                  'country',
                  'contact_number',
                  'address',
                  'legal_address']


class ProductListSerializer(ModelSerializer):
    product_group_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'product_group_name',
            'quantity'
        ]

    def get_product_group_name(self, obj):
        return obj.product_group.group


class ManufacturerDetailSerializer(ModelSerializer):
    manager = CustomUserSerializer(read_only=True)
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = [
            'id',
            'name',
            'country',
            'manager',
            'products'
        ]

    def get_products(self, obj):
        return ProductListSerializer(obj.product_set.filter(quantity__gt=0), many=True).data


class ManufacturerListSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country']


class ManufacturerCreateSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = [
            'name',
            "country",
        ]


class BrokerCompanyDetailSerializer(ModelSerializer):
    brokers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BrokerCompany
        fields = [
            'id',
            'monthly_fee',
            'contact_number',
            'brokers'
        ]

    def get_brokers(self, obj):
        brokers = Broker.objects.filter(brokerinfo__broker_company=obj)
        return BrokerSerializer(brokers, many=True).data


class CreateBrokerSerializer(serializers.Serializer):
    broker_id = serializers.IntegerField()
    monthly_fee = serializers.IntegerField()
    contact_number = serializers.CharField(max_length=20)


class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    product_group_name = serializers.CharField()
    production_date = serializers.DateField()
    quantity = serializers.IntegerField()
    expiry_period = serializers.IntegerField(required=False, allow_null=True)


class ProductSerializer(ModelSerializer):
    manufacturer = ManufacturerListSerializer(read_only=True)
    product_group = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'quantity',
            'production_date',
            'product_group',
            'expiry_period',
            'manufacturer'
        ]

    def get_product_group(self, obj):
        return obj.product_group.group


class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = BatchProduct
        fields = ['quantity', 'price_per_unit']


class BatchProductSerializer(ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = BatchProduct
        fields = [
            'id',
            'quantity',
            'price_per_unit',
            'product',
        ]



class OrderSerializer(ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    batches = serializers.SerializerMethodField(read_only=True)
    total_cost = serializers.SerializerMethodField(read_only=True)
    total_paid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'prepaid',
            'delivery_date',
            'status',
            'batches',
            'total_cost',
            'total_paid'
        ]

    def get_total_cost(self, obj):
        result = obj.batchproduct_set.annotate(batch_price=F('quantity') * F('price_per_unit')).aggregate(
            models.Sum('batch_price'))['batch_price__sum']
        return result

    def get_total_paid(self, obj):
        return obj.transaction_set.aggregate(models.Sum('amount'))['amount__sum']

    def get_status(self, obj):
        return obj.get_status_display()

    def get_batches(self, obj):
        return BatchProductSerializer(BatchProduct.objects.filter(batch=obj),
                                      many=True, read_only=True).data


class AlterOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'prepaid',
            'delivery_date',
        ]
