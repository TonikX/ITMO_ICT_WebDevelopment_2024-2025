# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API.

---

## **Описание endpoint-ов**

Получить информацию о всех сотрудниках авиакомпании

```
GET /airlines/<int:airline_pk>/employees
```

![](../assets/lab_3/airline_employees.png)

Получить информацию о бортах, принадлежащих авиакомпании, и статистику по маркам

1. Количество бортов
2. Минимальное и максимальное количество посадочных мест
3. Минимальная и максимальная скорость
4. Номера соответствующих бортов

```
GET /airlines/<int:pk>/plane-statistics/
```

![](../assets/lab_3/airline_planes_review.png)

Получить информацию о всех экипажах

```
GET /crews/
```

![](../assets/lab_3/crews.png)

Создать новый экипаж

```
POST /crews/
```

![](../assets/lab_3/crew_create.png)

Получить список всех перелетов

```
GET /flights/
```

![](../assets/lab_3/flights.png)

Создать новый перелет
```
POST /flights/
```

![](../assets/lab_3/flight_create.png)

Получить информацию о всех ремонтых работах и добавить новую

```
GET /maintenances/
```
```
POST /maintenances/
```

![](../assets/lab_3/maintenances.png)

Просмотреть самолеты, находящиеся в ремонте в данный момент

```
GET /planes/in-maintenance/
```

![](../assets/lab_3/panes_in_maintenance.png)

Просмотреть самолеты, наиболее часто летающие по заданному маршруту

```
GET /routes/<int:route_id>/most-frequent-plane/
```

![](../assets/lab_3/routes_most_frequent_plane.png)

Просмотреть маршруты, по которым летают рейсы, заполненные менее, чем на Х% (дефолтное значение = 50%)
```
GET /routes/under-filled/?threshold=X
```

![](../assets/lab_3/routes_underfilled.png)

Просмотреть все посадочные места на заданный рейс
```
GET /flights/<int:flight_pk>/seats/
```

![](../assets/lab_3/seats.png)

Просмотреть все свободные места на заданный рейс
```
GET /flights/<int:pk>/available-seats/
```

![](../assets/lab_3/seats_available.png)

Занять место на заданный рейс
```
POST /flights/<int:flight_pk>/sell-seat/
```

![](../assets/lab_3/seat_sell.png)

Просмотреть транзитные остановки рейса и добавить новую
```
GET /flights/<int:pk>/stops/
```
```
POST /flights/<int:pk>/stops/
```

![](../assets/lab_3/transit_stops.png)

## **Подключение Djoser**

Регистрация

```
POST /auth/users/
```

![](../assets/lab_3/register.png)

Получение токена

```
POST /auth/token/login/
```

![](../assets/lab_3/login.png)

Получение информации о текущем пользователе

```
GET /auth/users/me/
```

![](../assets/lab_3/get_me.png)

Создание сотрудника без авторизации

```
POST /airlines/<int:airline_pk>/employees
```

![](../assets/lab_3/employee_create_failed.png)

Создание сотрудника после авторизации

```
POST /airlines/<int:airline_pk>/employees
```

![](../assets/lab_3/employee_create_success.png)
