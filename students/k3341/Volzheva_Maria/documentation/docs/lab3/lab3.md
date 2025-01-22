# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов

### Individual Clients
##### 1. Получить список клиентов
```
GET /clients/
```

##### 2. Получить информацию о клиенте
```
GET /clients/{id}/
```

##### 3. Создать клиента
```
POST /clients/
```

#####4. Обновить клиента
```
PUT /clients/{id}/
```

#####5. Частично обновить клиента
```
PATCH /clients/{id}/
```

#####6. Удалить клиента
```
DELETE /clients/{id}/
```

### Agents
#####1. Получить список агентов
```
GET /agents/
```

#####2. Получить информацию об агенте
```
GET /agents/{id}/
```

#####3. Создать агента
```
POST /agents/
```

#####4. Обновить агента
```
PUT /agents/{id}/
```

#####5. Частично обновить агента
```
PATCH /agents/{id}/
```

#####6. Удалить агента
```
DELETE /agents/{id}/
```

### Individual Contracts
#####1. Получить список индивидуальных контрактов
```
GET /clients/contracts
```

#####2. Получить информацию об индивидуальном контракте
```
GET /clients/contracts/{id}/
```

#####3. Создать индивидуальный контракт
```
POST /clients/contracts
```

#####4. Обновить индивидуальный контракт
```
PUT /clients/contracts/{id}/
```

#####5. Частично обновить индивидуальный контракт
```
PATCH /clients/contracts/{id}/
```

#####6. Удалить индивидуальный контракт
```
DELETE /clients/contracts/{id}/
```

### Labor Contracts
#####1. Получить список трудовых контрактов
```
GET /agents/contracts/
```

#####2. Получить информацию о трудовом контракте
```
GET /agents/contracts/{id}/
```

#####3. Создать трудовой контракт
```
POST /agents/contracts/
```

#####4. Обновить трудовой контракт
```
PUT /agents/contracts/{id}/
```

#####5. Частично обновить трудовой контракт
```
PATCH /agents/contracts/{id}/
```

#####6. Удалить трудовой контракт
```
DELETE /agents/contracts/{id}/
```

### Organizations
#####1. Получить список организаций
```
GET /organizations/
```

#####2. Получить информацию об организации
```
GET /organizations/{id}/
```

#####3. Создать организацию
```
POST /organizations/
```

#####4. Обновить организацию
```
PUT /organizations/{id}/
```

#####5. Частично обновить организацию
```
PATCH /organizations/{id}/
```

#####6. Удалить организацию
```
DELETE /organizations/{id}/
```

### Collective Contracts
#####1. Получить список коллективных контрактов
```
GET /organizations/contracts/
```

#####2. Получить информацию о коллективном контракте
```
GET /organizations/contracts/{id}/
```

#####3. Создать коллективный контракт
```
POST /organizations/contracts/
```

#####4. Обновить коллективный контракт
```
PUT /organizations/contracts/{id}/
```

#####5. Частично обновить коллективный контракт
```
PATCH /organizations/contracts/{id}/
```

#####6. Удалить коллективный контракт
```
DELETE /organizations/contracts/{id}/
```

### Risk Categories
#####1. Получить список категорий рисков
```
GET /categories/
```

#####2. Создать категорию риска
```
POST /categories/
```

#####3. Обновить категорию риска
```
PUT /categories/{id}/
```

#####4. Частично обновить категорию риска
```
PATCH /categories/{id}/
```

#####5. Удалить категорию риска
```
DELETE /categories/{id}/
```

### Insured Employees
#####1. Получить список застрахованных сотрудников
```
GET /employees/
```

#####2. Получить информацию о застрахованном сотруднике
```
GET /employees/{id}/
```

#####3. Создать застрахованного сотрудника
```
POST /employees/
```

#####4. Обновить застрахованного сотрудника
```
PUT /employees/{id}/
```

#####5. Частично обновить застрахованного сотрудника
```
PATCH /employees/{id}/
```

#####6. Удалить застрахованного сотрудника
```
DELETE /employees/{id}/
```

### Insured Events
#####1. Получить список событий застрахованных сотрудников
```
GET /employees/events/
```

#####2. Создать событие застрахованного сотрудника
```
POST /employees/events/
```

### Payments
#####1. Получить список выплат застрахованных сотрудников
```
GET /employees/payments/
```

#####2. Создать выплату застрахованного сотрудника
```
POST /employees/payments/
```

### Other
#####1. Получить статистику по контрактам агентов
```
GET /agents/contracts/stats/
```

#####2. Получить информацию о связанных организациях
```
GET /organizations/related/
```

#####3. Получить отчёт по контрактам
```
GET /report/
```

#####4. Получить общую сумму выплат по типам договоров
```
GET /payments/total
```



### Auth
#####1. Получить токен юзера по паролю и никнейму
```
POST /auth/token/login
```
#####2. Вывести информацию о пользователе
```
GET /auth/users/me
```
#####3. Зарегистрировать пользователя
```
POST /auth/users
```

## Рассмотри листинг, связанный с агентами
##### models.py
``` python
class Agent(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    passport = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
``` 

##### serializers.py
``` python
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
``` 


##### views.py
``` python
class AgentAPIView(GenericAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer

    def get(self, request):
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AgentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()


class AgentContractStatsView(GenericAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Для каждого агента вывести количество заключенных им договоров каждого типа за определенный период времени",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Начало периода",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Конец периода",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval"),
        }
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        agents = Agent.objects.annotate(
            individual_contracts=Count('individualcontract', filter=(
                    Q(individualcontract__sign_date__gte=start_date) &
                    Q(individualcontract__sign_date__lte=end_date)
            )),
            collective_contracts=Count('collectivecontract', filter=(
                    Q(collectivecontract__sign_date__gte=start_date) &
                    Q(collectivecontract__sign_date__lte=end_date)
            ))
        ).values('first_name', 'second_name', 'patronymic', 'individual_contracts', 'collective_contracts')
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "statistics": [
                {
                    'agent': f"{agent['first_name']} {agent['second_name']} {agent['patronymic']}",
                    'individual_contracts_count': agent['individual_contracts'],
                    'collective_contracts_count': agent['collective_contracts']
                }
                for agent in agents
            ]
        }
        return Response(data, status=status.HTTP_200_OK)
``` 

##### urls.py
``` python
rom django.urls import path

from insurance_app.views import AgentAPIView, AgentDetailView, AgentContractStatsView ...

urlpatterns = [
...
    path('agents/', AgentAPIView.as_view()),
    path('agents/<int:pk>/', AgentDetailView.as_view()),
...
    path('agents/contracts/stats/', AgentContractStatsView.as_view()),
...
]
```

## Рассмотри работу эндпоинтов, связанных с агентами

![](images/1.PNG)

![](images/2.PNG)

![](images/3.PNG)

![](images/4.PNG)

![](images/5.PNG)

## Запуск программы:

```
python manage.py runserver
```
 