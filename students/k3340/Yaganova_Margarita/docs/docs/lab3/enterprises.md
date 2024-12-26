# Компании

## Сериализатор
```python
class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"


class EnterpriseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ["short_name"]
```

## Контроллеры
```python
class EnterpriseListCreateAPIView(generics.ListCreateAPIView):
    """
    Добавление и список компаний
    """
    queryset = Enterprise.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EnterpriseListSerializer
        elif self.request.method == 'POST':
            return EnterpriseSerializer


class EnterpriseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельной компанией: информация, изменение, удаление
    """
    queryset = Enterprise.objects.all()
    lookup_field = "id"
    serializer_class = EnterpriseSerializer
```

## Эндпоинты
1. GET "/enterprises/" - получение списка всех компаний
2. POST "/enterprises/"- добавление новой компании
3. GET "/enterprises/id/" - получение информации о конкретной компании
4. PUT/PATCH "/enterprises/id/" - изменение информации о компании
5. DELETE "/enterprises/id/" - удаление компании
