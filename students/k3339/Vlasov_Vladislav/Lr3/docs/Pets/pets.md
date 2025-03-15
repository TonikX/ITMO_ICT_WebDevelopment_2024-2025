## zoo/pets

По данному url возвращаются все животные в БД

Поскольку требуется вывести экземпляр модели, то используется ModelSerializer

```
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
        fields =  [
            "number",
            "name",
            "sex",
            "animal_type",
            "note_reptile_pet",
            "note_bird_pet",
            "birtday",
            "is_buy",
            "buy_pet",
            "is_rented",
            "rent_pet",
            "valliere", 
            "habited",
            "diet"
            ]

```
Как видно, для каждого из вложенных полей также используется сериализаторы на основе ModelSerializer


## Запрос к БД на базе CreateAPIView:

```
class CreatePetAPIView(CreateAPIView):
    serializer_class = PetCreateSerializer
    queryset = Pet.objects.all()
```