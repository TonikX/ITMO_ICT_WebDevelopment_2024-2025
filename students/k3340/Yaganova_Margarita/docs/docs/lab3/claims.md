# Страховые выплаты

## Сериализатор
```python
class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = "__all__"


class InsuranceClaimListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = ['insurance_contract', 'decision']
```

## Контроллеры
```python
class InsuranceClaimListCreateAPIView(generics.ListCreateAPIView):
    """
    Выплаты по страховым случаям
    """
    queryset = InsuranceClaim.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InsuranceClaimListSerializer
        elif self.request.method == "POST":
            return InsuranceClaimSerializer


class InsuranceClaimUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Изменение, просмотр, удаление конкретной выплаты по страховому случаю
    """
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer
    lookup_field = "id"
    

class EnterpriseInsuranceClaimsListView(generics.ListAPIView):
    """
    Выплаты по страховым случаям по конкретной компании
    """
    serializer_class = InsuranceClaimSerializer

    def get_queryset(self):
        enterprise_id = self.kwargs['id']
        return InsuranceClaim.objects.filter(insurance_contract__enterprise_id=enterprise_id)

```

## Эндпоинты
1. GET "/insurance_claims/ - получение списка всех страховых выплат
2. POST "/insurance_claims/"- добавление новой выплаты
3. GET "/insurance_claims/id/" - получение информации о конкретной выплате
4. PUT/PATCH "/insurance_claims/id/" - изменение информации о выплате
5. DELETE "/insurance_claims/id/" - удаление выплаты
6. GET "/insurance_claims/enterprise/id" - получение всех выплат по одной компании
