from rest_framework import serializers
from .models import *


class CountPetsInDepartSerializer(serializers.Serializer):
    
    depart = serializers.CharField(source='valliere__building__depart')
    count = serializers.IntegerField(source='number__count')


class RentPetSummarySerializer(serializers.Serializer):
    zoo = serializers.CharField(source='rent_pet__zoo')
    num_pets = serializers.IntegerField(source='number__count')
    cost = serializers.IntegerField(source='costs')


class RentOutZooPetSummarySerializer(serializers.Serializer):
    zoo = serializers.CharField(source='rent_pet__zoo')
    cost = serializers.IntegerField(source='costs_zoo')


class RentOutTypePetSummarySerializer(serializers.Serializer):
    animal_type = serializers.CharField()
    num_pets = serializers.IntegerField(source='count_type')
    cost = serializers.IntegerField(source='count_type')


class RentOutAllPetSummarySerializer(serializers.Serializer):
    num_all = serializers.IntegerField()
    cost_all = serializers.IntegerField()


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        exclude = ['pet']


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        exclude = ['pet']


class NoteReptileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteReptile
        exclude = ['pet']


class NoteBirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteBird
        exclude = ['pet']


class BuildingSerializer(serializers.ModelSerializer):
    
    type_build = serializers.CharField(source="get_type_build_display", read_only=True)

    class Meta:
        model = Building
        fields = "__all__"


class ValliereParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valliere_Parameter
        fields = "__all__"


class ValliereSerializer(serializers.ModelSerializer):
    
    building = BuildingSerializer()
    params = ValliereParameterSerializer(many=True)

    class Meta:
        model = Valliere
        fields = "__all__"


class HabitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habited
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class DietSerializer(serializers.ModelSerializer):
    
    products = ProductSerializer(many=True)

    class Meta:
        model = Diet
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    
    sex = serializers.CharField(source="get_sex_display", read_only=True)
    buy_pet = BuySerializer()
    rent_pet = RentSerializer()
    note_reptile_pet = NoteReptileSerializer()
    note_bird_pet = NoteBirdSerializer()
    valliere = ValliereSerializer()
    habited = HabitedSerializer()
    diet = DietSerializer()

    class Meta:
        model = Pet
        fields =  ["number", "name", "sex", "animal_type", "note_reptile_pet", "note_bird_pet", "birtday", "is_buy", "buy_pet", "is_rented", "rent_pet", "valliere", "habited", "diet"]



class PetCreateSerializer(serializers.ModelSerializer):
    
    buy_pet = BuySerializer(required=False)
    rent_pet = RentSerializer(required=False)
    note_reptile_pet = NoteReptileSerializer(required=False)
    note_bird_pet = NoteBirdSerializer(required=False)

    class Meta:
        model = Pet
        fields =  ["number", "name", "sex", "animal_type", "note_reptile_pet", "note_bird_pet", "birtday", "is_buy", "buy_pet", "is_rented", "rent_pet", "valliere", "habited", "diet"]

    def create(self, validated_data):

        buy_data = validated_data.pop("buy_pet", None)
        rent_data = validated_data.pop("rent_pet", None)
        note_reptile_data = validated_data.pop("note_reptile_pet", None)
        note_bird_data = validated_data.pop("note_bird_pet", None)

        if validated_data["is_buy"] == True:
            if buy_data is None:
                raise serializers.ValidationError("У купленных питомцев должна быть информация о покупке")

        if validated_data["is_rented"] is not None:
            if rent_data is None:
                raise serializers.ValidationError("У питомцев в аренде должна быть информация о аренде")

        if validated_data["animal_type"] == "reptile":
            if note_reptile_data is None:
                raise serializers.ValidationError("Рептилии должны иметь справку")
        
        if validated_data["animal_type"] == "bird":
            if note_bird_data is None:
                raise serializers.ValidationError("Птицы должы иметь справку")

        pet = Pet.objects.create(**validated_data)

        if validated_data["is_buy"] == True:
            Buy.objects.create(pet=pet, **buy_data)

        if validated_data["is_rented"] is not None:
            Rent.objects.create(pet=pet, **rent_data)

        if validated_data["animal_type"] == "reptile":
            NoteReptile.objects.create(pet=pet, **note_reptile_data)
        
        if validated_data["animal_type"] == "bird":
            NoteBird.objects.create(pet=pet, **note_bird_data)

        return pet