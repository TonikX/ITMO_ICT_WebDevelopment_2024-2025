from rest_framework import serializers
from .models import PrintShop, Newspaper, PrintRun, Delivery

# Сериализатор для PrintShop
class PrintShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintShop
        fields = '__all__'

# Сериализатор для Newspaper
class NewspaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newspaper
        fields = '__all__'

# Сериализатор для PrintRun
class PrintRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintRun
        fields = '__all__'

# Сериализатор для Delivery
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
