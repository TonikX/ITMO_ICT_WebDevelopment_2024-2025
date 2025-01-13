from rest_framework import serializers
from .models import Diet, Breed, Workshop, Cage, Hen, Employee


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    diet = DietSerializer()

    class Meta:
        model = Breed
        fields = '__all__'

class BreedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'

class CageSerializer(serializers.ModelSerializer):
    workshop = WorkshopSerializer()

    class Meta:
        model = Cage
        fields = '__all__'
    
class CageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = '__all__'

    def validate(self, data):
        workshop = data.get('workshop')
        row_number = data.get('row_number')

        if row_number > workshop.rows:
            raise serializers.ValidationError(
                f"Row number {row_number} exceeds the maximum rows ({workshop.rows}) in this workshop."
            )

        cage_number = data.get('cage_number')
        if Cage.objects.filter(
            workshop=workshop, row_number=row_number, cage_number=cage_number
        ).exists():
            raise serializers.ValidationError(
                f"Cage with row number {row_number} and cage number {cage_number} already exists in this workshop."
            )

        return data


class HenSerializer(serializers.ModelSerializer):
    breed = BreedSerializer()
    cage = CageSerializer()

    class Meta:
        model = Hen
        fields = '__all__'

class HenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hen
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    assigned_cages = CageSerializer(many=True)

    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

