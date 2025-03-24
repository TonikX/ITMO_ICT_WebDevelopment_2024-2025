# Отчет по лабораторной работе 3

## Задание
Данный отчет описывает разработку и функциональность системы диспетчеризации автобусов, реализованной с использованием Django и Django REST Framework. В системе предусмотрены модели для автобусов, водителей, маршрутов и смен, а также API для управления данными.

## Структура проекта
Проект состоит из следующих основных компонентов:

- **Модели**: Определяют структуру данных.
- **Сериализаторы**: Преобразуют данные моделей в формат JSON и обратно.
- **Представления**: Обрабатывают HTTP-запросы и возвращают ответы.
- **URL-ы**: Определяют маршруты для API.
- **Админка**: Позволяет управлять данными через интерфейс администратора.

## Административная панель
Административная панель позволяет управлять следующими сущностями:
- Типы автобусов (BusCategory)
- Автобусы (Bus)
- Водители (Driver)
- Маршруты (Route)
- Смены (Shift)

Регистрация моделей в административной панели:
```python
from django.contrib import admin
from .models import BusCategory, Bus, Driver, Route, Shift

admin.site.register(BusCategory)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(Shift)
```

## Модели данных

### Тип автобуса (BusCategory)
Определяет вместимость и тип автобуса.
```python
class BusCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveSmallIntegerField()
```

### Автобус (Bus)
Автобус привязан к категории и имеет регистрационный номер.
```python
class Bus(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(BusCategory, on_delete=models.PROTECT)
    
    @property
    def capacity(self):
        return self.category.capacity  # Вместимость берётся из категории
```

### Водитель (Driver)
Содержит личные данные и позволяет рассчитать зарплату водителя.
```python
class Driver(models.Model):
    passport_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=40, verbose_name="ФИО")

    CLASS_I = 'I'
    CLASS_II = 'II'
    CLASS_III = 'III'
    CLASS_CHOICES = [
        (CLASS_I, 'I класс'),
        (CLASS_II, 'II класс'),
        (CLASS_III, 'III класс'),
    ]

    driver_class = models.CharField(max_length=3, choices=CLASS_CHOICES)
    experience = models.PositiveSmallIntegerField(help_text="Стаж работы в годах")

    BASE_SALARY = {
        CLASS_I: 50000,
        CLASS_II: 60000,
        CLASS_III: 70000,
    }
    EXPERIENCE_BONUS = 1000  # Доплата за каждый год стажа

    @property
    def salary(self):
        """Оклад зависит от категории и стажа"""
        base = self.BASE_SALARY.get(self.driver_class, 50000)
        return base + (self.experience * self.EXPERIENCE_BONUS)
```

### Маршрут (Route)
Описание маршрута с расписанием.
```python
class Route(models.Model):
    route_number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
```

### Смена (Shift)
Позволяет водителю работать на определенном маршруте в указанное время.
```python
class Shift(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    ACTIVE = 'Active'
    BROKEN_DOWN = 'Breakdown'
    NO_DRIVER = 'No Driver'
    STATUS_CHOICES = [
        (ACTIVE, 'Отработано'),
        (BROKEN_DOWN, 'Поломка автобуса'),
        (NO_DRIVER, 'Нет водителя'),
    ]

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ACTIVE)
    reason = models.TextField(null=True, blank=True)
```

## API и сериализация данных

Для работы с данными используется Django REST Framework. Пример сериализатора для автобусов:
```python
class BusSerializer(serializers.ModelSerializer):
    capacity = serializers.ReadOnlyField()

    class Meta:
        model = Bus
        fields = '__all__'
```
## Представления (Views)
Представления реализуют логику обработки запросов. Ниже приведены примеры представлений и их описание.

**CRUD-запросы для автобусов**
```python
class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class BusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
```

**CRUD-запросы для водителей**
```python
class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
```

**CRUD-запросы для маршрута**
```python
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
```

**CRUD-запросы для смен**
```python
class ShiftListCreateView(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class ShiftRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
```

**Аналитические запросы**
```python
# Список водителей на маршруте с их графиком работы
class DriversOnRouteView(APIView):
    def get(self, request, route_id):
        shifts = Shift.objects.filter(route_id=route_id).select_related('driver')
        data = [
            {
                "driver": shift.driver.full_name,
                "shift_date": shift.shift_date,
                "start_time": shift.start_time,
                "end_time": shift.end_time
            }
            for shift in shifts
        ]
        return Response(data)


# Общая протяженность всех маршрутов
class TotalRouteDistanceView(APIView):
    def get(self, request):
        total_distance = Route.objects.aggregate(total=Sum('duration_minutes'))['total'] or 0
        return Response({"total_route_duration": total_distance})


# Автобусы, не вышедшие на линию
class InactiveBusesView(APIView):
    def get(self, request, date):
        breakdown_shifts = Shift.objects.filter(shift_date=date, status="Breakdown")
        data = [
            {
                "route": shift.route.route_number,
                "bus": shift.bus.registration_number,
                "driver": shift.driver.full_name,
                "status": shift.status,
                "reason": shift.reason
            }
            for shift in breakdown_shifts
        ]
        return Response(data)


# Водители, не вышедшие на линию
class InactiveDriversView(APIView):
    def get(self, request, date):
        no_driver_shifts = Shift.objects.filter(shift_date=date, status="No Driver")
        data = [
            {
                "route": shift.route.route_number,
                "driver": shift.driver.full_name,
                "bus": shift.bus.registration_number,
                "status": shift.status,
                "reason": shift.reason
            }
            for shift in no_driver_shifts
        ]
        return Response(data)


# Время начала и окончания движения автобусов на маршрутах
class RouteScheduleView(APIView):
    def get(self, request):
        routes = Route.objects.all()
        data = []
        for route in routes:
            shifts = Shift.objects.filter(route=route).order_by("start_time")
            if shifts.exists():
                data.append({
                    "route": route.route_number,
                    "first_bus_start": shifts.first().start_time,
                    "last_bus_end": shifts.last().end_time
                })
        return Response(data)


# Количество водителей каждого класса
class DriverCategoryCountView(APIView):
    def get(self, request):
        driver_counts = Driver.objects.values("driver_class").annotate(count=Count("id"))
        return Response({"drivers_by_category": list(driver_counts)})


# Отчет о состоянии автопарка, включая количество автобусов по типам, маршруты и водителей.
class ReportView(APIView):
    def get(self, request):
        # Сгруппировать автобусы по категориям и посчитать количество автобусов, маршрутов и водителей
        bus_types = Bus.objects.values('category__name').annotate(
            bus_count=Count('id'),  # Количество автобусов
            route_count=Count('shift__route', distinct=True),  # Количество уникальных маршрутов, обслуживаемых автобусами
            driver_count=Count('shift__driver', distinct=True),  # Количество уникальных водителей, обслуживающих эти автобусы
        )

        # Суммарная протяженность всех маршрутов
        total_duration = Route.objects.aggregate(total_duration=Sum('duration_minutes'))['total_duration']

        # Статистика по водителям: средний стаж и общее количество водителей
        driver_stats = Driver.objects.aggregate(
            avg_experience=Avg('experience'),  # Средний стаж водителей
            total_count=Count('id')  # Общее количество водителей
        )

        # Получаем список маршрутов с их характеристиками, включая автобусы и водителей
        route_details = Route.objects.annotate(
            bus_count=Count('shift__bus', distinct=True),  # Количество автобусов на маршруте
            driver_count=Count('shift__driver', distinct=True)  # Количество водителей на маршруте
        ).values('route_number', 'start_point', 'end_point', 'bus_count', 'driver_count', 'duration_minutes')

        # Формируем отчет
        report = {
            'bus_types': list(bus_types),  # Сгруппированные данные по типам автобусов
            'total_route_duration': total_duration,  # Суммарная длительность маршрутов
            'driver_stats': driver_stats,  # Статистика по водителям
            'route_details': list(route_details)  # Детали по маршрутам
        }

        # Возвращаем отчет в виде JSON
        return Response(report)
```

## API эндпоинты
### CRUD запросы для моделей

1. **Типы автобусов**
   - `GET /bus-categories/` — Получить список всех типов автобусов.
   - `POST /bus-categories/` — Создать новый тип автобуса.
   - `GET /bus-categories/<int:pk>/` — Получить информацию о конкретном типе автобуса.
   - `PUT /bus-categories/<int:pk>/` — Обновить информацию о типе автобуса.
   - `DELETE /bus-categories/<int:pk>/` — Удалить тип автобуса.

2. **Автобусы**
   - `GET /buses/` — Получить список всех автобусов.
   - `POST /buses/` — Создать новый автобус.
   - `GET /buses/<int:pk>/` — Получить информацию о конкретном автобусе.
   - `PUT /buses/<int:pk>/` — Обновить информацию о автобусе.
   - `DELETE /buses/<int:pk>/` — Удалить автобус.

3. **Водители**
   - `GET /drivers/` — Получить список всех водителей.
   - `POST /drivers/` — Создать нового водителя.
   - `GET /drivers/<int:pk>/` — Получить информацию о конкретном водителе.
   - `PUT /drivers/<int:pk>/` — Обновить информацию о водителе.
   - `DELETE /drivers/<int:pk>/` — Удалить водителя.

4. **Маршруты**
   - `GET /routes/` — Получить список всех маршрутов.
   - `POST /routes/` — Создать новый маршрут.
   - `GET /routes/<int:pk>/` — Получить информацию о конкретном маршруте.
   - `PUT /routes/<int:pk>/` — Обновить информацию о маршруте.
   - `DELETE /routes/<int:pk>/` — Удалить маршрут.

5. **Смены**
   - `GET /shifts/` — Получить список всех смен.
   - `POST /shifts/` — Создать новую смену.
   - `GET /shifts/<int:pk>/` — Получить информацию о конкретной смене.
   - `PUT /shifts/<int:pk>/` — Обновить информацию о смене.
   - `DELETE /shifts/<int:pk>/` — Удалить смену.

### Аналитические запросы

1. **Водители на маршруте**
   - `GET /routes/<int:route_id>/drivers/` — Получить список водителей на указанном маршруте и их графики.

2. **Общая продолжительность маршрутов**
   - `GET /routes/total-duration/` — Получить суммарную продолжительность всех маршрутов.

3. **Автобусы, не вышедшие на линию**
   - `GET /buses/inactive/<str:date>/` — Получить список автобусов, которые не вышли на линию в указанную дату.

4. **Водители, не вышедшие на линию**
   - `GET /drivers/inactive/<str:date>/` — Получить список водителей, которые не вышли на линию в указанную дату.

5. **Время начала и окончания движения автобусов**
   - `GET /routes/schedule/` — Получить время начала и окончания движения автобусов по маршрутам.

6. **Количество водителей по категориям**
   - `GET /drivers/category-count/` — Получить количество водителей по категориям (например, водитель категории A, B и т.д.).

7. **Отчет о состоянии автопарка**
   - `GET /reports/park-status/` — Получить отчет о состоянии автопарка, включая количество автобусов по типам, маршруты и водителей.

## Валидация смен
В системе реализована проверка пересечения смен у водителей и автобусов.
```python
def validate(self, data):
    shift_date = data["shift_date"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    bus = data.get("bus")
    driver = data.get("driver")
    status = data.get("status")
    
    if driver and status == "Active":
        overlapping_driver_shifts = Shift.objects.filter(
            shift_date=shift_date,
            driver=driver,
            status="Active",
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if overlapping_driver_shifts.exists():
            raise serializers.ValidationError("Этот водитель уже работает в другой смене в это время.")
    return data
```

## Вывод
Разработанная система позволяет эффективно управлять автобусным парком, отслеживать маршруты и смены водителей.

