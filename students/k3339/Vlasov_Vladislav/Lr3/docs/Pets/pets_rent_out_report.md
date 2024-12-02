## zoo/pets_rent_out/report

По данному url собираетяс отчёт, содержащий информацию о сданных в аренду животных.
В данном отчёте присутвует следующая информаци:

* Общее количество по виду
* Общая стоимость по виду
* Общая стоимость оренды по зоопарку
* Общяя стоимость сданных животных
* Общее количество сданных животных


Для отображения информации используется аж 4 сериализатора, поскольку требуется собрать несколько QwerySet

```
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
```

## Запрос к БД на базе APIView:

```
class GetReportOutRentAPIView(APIView):
    def get(self, request):
        pets_outrent_type = Pet.objects.filter(is_rented="out").values("animal_type").annotate(count_type=Count("number"), costs_type=Sum("rent_pet__price"))
        pets_outrent_zoo = Pet.objects.filter(is_rented="out").values("rent_pet__zoo").annotate(costs_zoo=Sum("rent_pet__price"))
        pets_outrent_all = Pet.objects.filter(is_rented="out").aggregate(num_all=Count("number"), cost_all=Sum("rent_pet__price"))        

        #print(pets_outrent_report)
        serializer1 = RentOutTypePetSummarySerializer(pets_outrent_type, many=True)
        serializer2 = RentOutZooPetSummarySerializer(pets_outrent_zoo, many=True)
        serializer3 = RentOutAllPetSummarySerializer(pets_outrent_all)

        return Response({"RentedPets1": serializer1.data, "RentedPets2": serializer2.data, "RentedPets3": serializer3.data})
```