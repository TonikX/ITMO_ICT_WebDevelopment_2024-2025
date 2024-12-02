## zoo/valliers_empty

По данному url выводится список пустых вольеров.

Поскольку требуется вывести экземпляр модели, то используется ModelSerializer

```
class ValliereSerializer(serializers.ModelSerializer):
    
    building = BuildingSerializer()
    params = ValliereParameterSerializer(many=True)

    class Meta:
        model = Valliere
        fields = "__all__"
```

## Запрос к БД на базе ListAPIView:

```
class GetEmptyValliersAPIView(ListAPIView):
    serializer_class = ValliereSerializer
    queryset = Valliere.objects.annotate(Count("pets")).filter(pets__count=0)
```