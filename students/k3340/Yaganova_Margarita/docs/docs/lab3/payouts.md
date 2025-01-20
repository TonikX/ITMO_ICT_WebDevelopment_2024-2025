# Возможные выплаты по категориям

## Сериализатор
```python
class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = '__all__'


class PayoutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ['risk_category', 'insured_event']
```

## Контроллеры
```python
class PayoutListCreateAPIView(generics.ListCreateAPIView):
    """
    Список и добавление возможных выплат по категориям
    """
    queryset = Payout.objects.all()

    def get_serializer_class(self):
        if self.request.method =="GET":
            return PayoutListSerializer
        elif self.request.method == "POST":
            return PayoutSerializer


class PayoutUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Обновление информации, её просмотр и удаление конкретной выплаты
    """
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    lookup_field = "id"
```

## Эндпоинты
1. GET "/payouts/" - получение списка всех возможных выплат
2. POST "/payouts/"- добавление новой выплаты
3. GET "/payouts/id/" - получение информации о конкретной выплате
4. PUT/PATCH "/payouts/id/" - изменение информации о выплате
5. DELETE "/payouts/id/" - удаление выплаты
