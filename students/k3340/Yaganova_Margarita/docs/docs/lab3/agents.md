# Страховые агенты

## Сериализатор
```python
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"


class AgentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["username"]
```

## Контроллеры
```python
class AgentListAPIView(generics.ListAPIView):
    """
    Получение списка агентов
    Добавление происходит через регистрацию по токенам
    """
    queryset = Agent.objects.all()
    serializer_class = AgentListSerializer


class AgentDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление агента
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    lookup_field = "id"


class ActiveAgentsListView(generics.ListAPIView):
    """
    Список активных агентов на данный момент
    """
    serializer_class = AgentListSerializer

    def get_queryset(self):
        return Agent.objects.filter(contract__start_date__lte=timezone.now(),
                                    contract__end_date__gte=timezone.now())
```

## Эндпоинты
1. GET "/agents/" - получение списка всех страховых агентов
2. POST "/auth/users/"- регистрация нового страхового агента
3. POST "/auth/token/login/" - авторизация страхового агента
4. GET "/auth/users/me/" - получение информации о страховом агенте
5. PATCH "/auth/users/me/" - изменение информации об агенте
6. DELETE "/agents/id/" - удаление страхового агента
7. GET "/agents/active/" - получение списка действующих агентов
