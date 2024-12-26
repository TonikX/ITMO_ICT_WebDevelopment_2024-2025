from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import *


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'patronymic', 'role']


# Пользователи
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'patronymic', 'email', 'role']


class UserDetailSerializer(UserSerializer):
    newspapers = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['newspapers']

    def get_newspapers(self, obj):
        if obj.role == 'editor':
            return NewspaperSerializer(obj.newspapers.all(), many=True).data
        return []


# Газеты
class NewspaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newspaper
        fields = ['id', 'name', 'index', 'price', 'editor']


class NewspaperDetailSerializer(NewspaperSerializer):
    editions = serializers.SerializerMethodField()
    distributions = serializers.SerializerMethodField()

    class Meta(NewspaperSerializer.Meta):
        fields = NewspaperSerializer.Meta.fields + ['editions', 'distributions']

    def get_editions(self, obj):
        return EditionSerializer(obj.editions.all(), many=True).data

    def get_distributions(self, obj):
        return DistributionSerializer(obj.distributions.all(), many=True).data


# Типографии
class PrintingHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintingHouse
        fields = ['id', 'name', 'address', 'is_active']


class PrintingHouseDetailSerializer(PrintingHouseSerializer):
    editions = serializers.SerializerMethodField()
    distributions = serializers.SerializerMethodField()

    class Meta(PrintingHouseSerializer.Meta):
        fields = PrintingHouseSerializer.Meta.fields + ['editions', 'distributions']

    def get_editions(self, obj):
        return EditionSerializer(obj.editions.all(), many=True).data

    def get_distributions(self, obj):
        return DistributionSerializer(obj.distributions.all(), many=True).data


# Почтовые отделения
class PostOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = ['id', 'number', 'address']


class PostOfficeDetailSerializer(PostOfficeSerializer):
    distributions = serializers.SerializerMethodField()

    class Meta(PostOfficeSerializer.Meta):
        fields = PostOfficeSerializer.Meta.fields + ['distributions']

    def get_distributions(self, obj):
        return DistributionSerializer(obj.distributions.all(), many=True).data


# Тиражи
class EditionSerializer(serializers.ModelSerializer):
    printing_house_name = serializers.ReadOnlyField(source='printing_house.name')
    newspaper_name = serializers.ReadOnlyField(source='newspaper.name')

    class Meta:
        model = Edition
        fields = ['id', 'printing_house', 'printing_house_name', 'newspaper', 'newspaper_name', 'quantity']


# Поставки
class DistributionSerializer(serializers.ModelSerializer):
    post_office_address = serializers.ReadOnlyField(source='post_office.address')
    printing_house_name = serializers.ReadOnlyField(source='printing_house.name')
    newspaper_name = serializers.ReadOnlyField(source='newspaper.name')

    class Meta:
        model = Distribution
        fields = [
            'id',
            'post_office',
            'post_office_address',
            'printing_house',
            'printing_house_name',
            'newspaper',
            'newspaper_name',
            'quantity'
        ]
