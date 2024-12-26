# Клиенты

## Сериализатор
```python
class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
```

## Контроллеры
```python
class ClientListCreateView(generics.ListCreateAPIView):
    """
    Получение полного списка клиентов (GET запрос),
    а также  добавление клиентов (POST запрос)
    """
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientListSerializer
        elif self.request.method == 'POST':
            return ClientSerializer


class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельными клиентами: вывод информации,
    редактирование, удаление
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = "id"
```

## Эндпоинты
1. GET "/clients/" - получение списка всех клиентов
2. POST "/clients/"- добавление нового клиента
3. GET "/clients/id/" - получение информации о конкретном клиенте
4. PUT/PATCH "/clients/id/" - изменение информации о клиенте
5. DELETE "/clients/id/" - удаление клиента
