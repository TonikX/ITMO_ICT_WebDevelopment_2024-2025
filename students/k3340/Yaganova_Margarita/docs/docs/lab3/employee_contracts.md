# Трудовые договоры с агентами

## Сериализатор
```python
class EmploymentContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentContract
        fields = "__all__"
```

## Контроллеры
```python
class EmployeeContractListCreateAPIView(generics.ListCreateAPIView):
    """
    Получение информации о списке контрактов с агентами, а также их добавление
    """
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer


class EmployeeContractUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельным рабочим контрактом: просмотр, редактирование, удаление
    """
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
    lookup_field = "id"
```

## Эндпоинты
1. GET "/employee_contracts/" - получение списка всех трудовых договоров
2. POST "/clients/"- добавление нового трудового договора
3. GET "/clients/id/" - получение информации о конкретном трудовом договоре
4. PUT/PATCH "/clients/id/" - изменение информации о трудовом договоре
5. DELETE "/clients/id/" - удаление трудового договора
