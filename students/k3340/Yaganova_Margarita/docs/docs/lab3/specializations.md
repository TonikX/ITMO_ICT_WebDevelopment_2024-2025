# Специализации

## Сериализатор
```python
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"
```

## Контроллеры
```python
class SpecializationListCreateAPIView(generics.ListCreateAPIView):
    """
    Добавление и список всех возможных специализаций компаний
    """
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
```

## Эндпоинты
1. GET "/specializations/" - получение списка всех специализаций
2. POST "/specializations/"- добавление новой специализации
