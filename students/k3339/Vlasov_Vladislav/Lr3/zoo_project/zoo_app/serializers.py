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


class DietCudSerializer(serializers.ModelSerializer):

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

    def my_validate(self, validated_data, buy_data, rent_data, note_reptile_data, note_bird_data, is_rented):
        if validated_data["is_buy"] == True:
            if buy_data is None:
                raise serializers.ValidationError("У купленных питомцев должна быть информация о покупке")
        else:
            if buy_data is not None:
                raise serializers.ValidationError("У купленных питомцев не должно быть информации о покупке")

        if is_rented is not None:
            if rent_data is None:
                raise serializers.ValidationError("У питомцев в аренде должна быть информация о аренде")
        else:
            if rent_data is not None:
                raise serializers.ValidationError("У питомцев не в аренде не должно быть информации о аренде")

        if validated_data["animal_type"] == "reptile":
            if note_reptile_data is None:
                raise serializers.ValidationError("Рептилии должны иметь справку")
            
            if note_bird_data is not None:
                raise serializers.ValidationError("Рептилии не должы иметь справку птиц")
        
        elif validated_data["animal_type"] == "bird":
            if note_bird_data is None:
                raise serializers.ValidationError("Птицы должы иметь справку")
            
            if note_reptile_data is not None:
                raise serializers.ValidationError("Птицы не должны иметь справку рептилий")
        
        else:
            if note_bird_data is not None or note_reptile_data is not None:
                raise serializers.ValidationError("Эти животные не должы иметь справку")

    def create(self, validated_data):

        buy_data = validated_data.pop("buy_pet", None)
        rent_data = validated_data.pop("rent_pet", None)
        note_reptile_data = validated_data.pop("note_reptile_pet", None)
        note_bird_data = validated_data.pop("note_bird_pet", None)
        is_rented = validated_data.pop("is_rented", None)

        self.my_validate(validated_data, buy_data, rent_data, note_reptile_data, note_bird_data, is_rented)

        pet = Pet.objects.create(**validated_data)
        pet.is_rented = is_rented

        if validated_data["is_buy"] == True:
            Buy.objects.create(pet=pet, **buy_data)

        if is_rented is not None:
            Rent.objects.create(pet=pet, **rent_data)

        if validated_data["animal_type"] == "reptile":
            NoteReptile.objects.create(pet=pet, **note_reptile_data)
        
        if validated_data["animal_type"] == "bird":
            NoteBird.objects.create(pet=pet, **note_bird_data)

        return pet
    
    def update(self, instance, validated_data):

        buy_data = validated_data.pop("buy_pet", None)
        rent_data = validated_data.pop("rent_pet", None)
        note_reptile_data = validated_data.pop("note_reptile_pet", None)
        note_bird_data = validated_data.pop("note_bird_pet", None)
        is_rented = validated_data.pop("is_rented", None)

        self.my_validate(validated_data, buy_data, rent_data, note_reptile_data, note_bird_data, is_rented)

        for attr, value in validated_data.items():
            if attr not in ["note_bird_pet", "note_reptile_pet", "buy_pet", "rent_pet"]:
                setattr(instance, attr, value)
        
        instance.is_rented = is_rented
        instance.save()

        if validated_data["is_buy"] == True:
            for attr, value in buy_data.items():
                setattr(instance.buy_pet, attr, value)
            instance.buy_pet.save()

        if is_rented is not None:
            for attr, value in rent_data.items():
                setattr(instance.rent_pet, attr, value)
            instance.rent_pet.save()

        if validated_data["animal_type"] == "reptile":
            for attr, value in note_reptile_data.items():
                setattr(instance.note_reptile_pet, attr, value)
            instance.note_reptile_pet.save()
        
        if validated_data["animal_type"] == "bird":
            for attr, value in note_bird_data.items():
                setattr(instance.note_bird_pet, attr, value)
            instance.note_bird_pet.save()

        return instance