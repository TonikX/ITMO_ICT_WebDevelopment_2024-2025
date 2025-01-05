## zoo/pets_rent_in/state

По данному url для каждого из зоопарков, предоставивших животных в аренду, выводится общее
количество животных в аренде и их общая стоимость.

Поскольку собираемая в запросе информация не соответсвует какой-либо модели, то для её вывода используется простой сериализатор:

```
class RentPetSummarySerializer(serializers.Serializer):
    zoo = serializers.CharField(source='rent_pet__zoo')
    num_pets = serializers.IntegerField(source='number__count')
    cost = serializers.IntegerField(source='costs')
```

## Запрос к БД на базе APIView:

```
rents = Pet.objects
            .filter(is_rented="in")
            .values("rent_pet__zoo")
            .annotate(Count("number"), costs=Sum("rent_pet__price"))
```