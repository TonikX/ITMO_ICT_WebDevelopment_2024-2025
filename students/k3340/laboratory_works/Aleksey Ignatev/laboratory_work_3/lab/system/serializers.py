from rest_framework import serializers
from .models import *


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CountAnimalInArea(serializers.ModelSerializer):
    count_animals_in = serializers.SerializerMethodField()
    animals_in = serializers.SerializerMethodField()

    class Meta:
        model = Area
        fields = ['id', 'name', 'count_animals_in', 'animals_in']

    def get_count_animals_in(self, obj):
        # Filter cages whose building is in the given area
        aias = AnimalInCage.objects.filter(cage__building__area=obj)
        # Count animals associated with those cages
        return Animal.objects.filter(where__in=aias).distinct().count()

    def get_animals_in(self, obj):
        # Filter cages whose building is in the given area
        aias = AnimalInCage.objects.filter(cage__building__area=obj)
        # Get all distinct animals in those cages
        qs = Animal.objects.filter(where__in=aias).distinct()
        ser = AnimalSerializer(qs, many=True)
        return ser.data

class CageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = '__all__'


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = '__all__'


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'


class WinterPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinterPlace
        fields = '__all__'


class AnimalInCageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalInCage
        fields = '__all__'
