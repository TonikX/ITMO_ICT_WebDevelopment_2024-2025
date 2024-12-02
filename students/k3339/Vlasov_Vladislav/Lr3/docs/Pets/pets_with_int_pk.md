## zoo/pets_with/<int:pk>

По данному url для заданного животного ввыводится список животных, размещенных в том же
здании, что и это животное.

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


## Запрос к БД на базе ListAPIView:

```
class GetPetsTogetherAPIView(ListAPIView):
   serializer_class = PetSerializer
   def get_queryset(self):
        pk = self.kwargs.get('pk')
        building = Pet.objects.get(number=pk).valliere.building.id
        return Pet.objects.filter(valliere__building__id=building).exclude(number=pk)
```

Фактически к БД выполняется 2 запроса. Первый для получения id здания, в котром проживает животное, а второй - для вывода всех животных в это здании (кроме заданного)