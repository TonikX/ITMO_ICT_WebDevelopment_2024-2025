from rest_framework import serializers
from .models import (
    Habitat, Department, Building, Enclosure, Staff, Animal,
    FeedingRationType, FeedingRation, Zoo, WinteringPlace,
    FeedingHistory, CaretakerAssignment, VeterinarianAssignment,
    TransferHistory
)

# ----------------------------------------------------------------------
# Базовые сериализаторы для всех моделей
# ----------------------------------------------------------------------

class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Building
        fields = '__all__'


class EnclosureSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)

    class Meta:
        model = Enclosure
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class FeedingRationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingRationType
        fields = '__all__'


class FeedingRationSerializer(serializers.ModelSerializer):
    ration_type_name = serializers.CharField(source='ration_type.name', read_only=True)

    class Meta:
        model = FeedingRation
        fields = '__all__'


class ZooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zoo
        fields = '__all__'


class WinteringPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinteringPlace
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    # Дополнительные поля для удобства отображения
    habitat_name = serializers.CharField(source='habitat.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    enclosure_number = serializers.CharField(source='current_enclosure.number', read_only=True)
    owner_zoo_name = serializers.CharField(source='owner_zoo.name', read_only=True)

    class Meta:
        model = Animal
        fields = '__all__'


class FeedingHistorySerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    ration_name = serializers.CharField(source='ration.name', read_only=True)

    class Meta:
        model = FeedingHistory
        fields = '__all__'


class CaretakerAssignmentSerializer(serializers.ModelSerializer):
    caretaker_name = serializers.CharField(source='caretaker.full_name', read_only=True)
    animal_name = serializers.CharField(source='animal.name', read_only=True)

    class Meta:
        model = CaretakerAssignment
        fields = '__all__'


class VeterinarianAssignmentSerializer(serializers.ModelSerializer):
    veterinarian_name = serializers.CharField(source='veterinarian.full_name', read_only=True)
    animal_name = serializers.CharField(source='animal.name', read_only=True)

    class Meta:
        model = VeterinarianAssignment
        fields = '__all__'


class TransferHistorySerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    from_enclosure_number = serializers.CharField(source='from_enclosure.number', read_only=True)
    to_enclosure_number = serializers.CharField(source='to_enclosure.number', read_only=True)

    class Meta:
        model = TransferHistory
        fields = '__all__'