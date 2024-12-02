## zoo/pets_in_departs
По данному url для каждого отдела зоопарка выводится общее количество животных в отделе.

Поскольку собираемая в запросе информация не соответсвует какой-либо модели, то для её вывода используется простой сериализатор:

```
class CountPetsInDepartSerializer(serializers.Serializer):
    
    depart = serializers.CharField(source='valliere__building__depart')
    count = serializers.IntegerField(source='number__count')
```

## Запрос к БД на базе APIView:

```
departs = Pet.objects.values("valliere__building__depart").annotate(Count("number"))
```