# Страховые договоры

## Сериализатор
```python
class InsuranceContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceContract
        fields = "__all__"


class InsuranceContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceContract
        fields = ['agent', 'enterprise']
```

## Контроллеры
```python
class InsuranceContractListCreateAPIView(generics.ListCreateAPIView):
    """
    Список и добавление страховых договоров
    """
    queryset = InsuranceContract.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InsuranceContractListSerializer
        elif self.request.method == "POST":
            return InsuranceContractSerializer


class InsuranceContractUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельным страховым договором
    """
    queryset = InsuranceContract.objects.all()
    serializer_class = InsuranceContractSerializer
    lookup_field = "id"




class EnterpriseContractsListView(generics.ListAPIView):
    """
    Список страховых договоров по конкретной компании
    """
    serializer_class = InsuranceContractSerializer

    def get_queryset(self):
        enterprise_id = self.kwargs['id']
        return InsuranceContract.objects.filter(enterprise_id=enterprise_id)


class AgentContractsListView(generics.ListAPIView):
    """
    Список страховых договоров, заключенных конкретным агентом
    """
    serializer_class = AgentListSerializer

    def get_queryset(self):
        agent_id = self.kwargs['id']
        return InsuranceContract.objects.filter(agent_id=agent_id)


class SpecializationContractsListView(generics.ListAPIView):
    """
    Страховые договоры с компаниями определенной специализации
    """
    serializer_class = InsuranceContractSerializer

    def get_queryset(self):
        specialization_id = self.kwargs['id']
        return InsuranceContract.objects.filter(enterprise__specialization_id=specialization_id)


class ClientContractsListView(generics.ListAPIView):
    """
    Список страховых договоров, в которых участвует конкретный пользователь
    """
    serializer_class = InsuranceContractSerializer

    def get_queryset(self):
        client_id = self.kwargs['id']
        return InsuranceContract.objects.filter(clients__id=client_id)
```

## Эндпоинты
1. GET "/contracts/" - получение списка всех страховых договоров
2. POST "/contracts/"- добавление нового договора
3. GET "/contracts/id/" - получение информации о конкретном договоре
4. PUT/PATCH "/contracts/id/" - изменение информации о договоре
5. DELETE "/contracts/id/" - удаление договора
6. GET "/contracts/enterprise/id/" - получение списка всех страховых договоров по конкретной компании
7. GET "/contracts/agent/id/" - получение списка всех страховых договоров, заключенных определенным агентом
8. GET "/contracts/specialization/id/" - получение списка страховых договоров по определенной специализации компаний
9. GET "/contracts/client/id/" - получение списка договоров, в которых участвует отдельный клиент
