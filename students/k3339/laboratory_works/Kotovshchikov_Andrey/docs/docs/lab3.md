# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API.

---

## **Описание endpoint-ов из задания**

Получить информацию о клиентах, проживавших в заданном номере, в заданный период времени

```
GET /hotel/rooms/<id номера>/guests/
```

![](assets/lab3/guests_at_room.png)

Получить информацию о клиентах, прибывших из заданного города

```
GET /hotel/guests/
```

![](assets/lab3/guests_from_city.png)

Получить информацию о том, кто из служащих убирал номер указанного клиента в заданный день недели

```
GET /hotel/employees/
```

![](assets/lab3/employees.png)

Получить информацию о свободных номерах в гостинице

```
GET /hotel/rooms/
```

![](assets/lab3/rooms.png)

Получить список клиентов с указанием места жительства, которые проживали в те же дни,
что и заданный клиент, в определенный период времени

```
GET /hotel/guests/<id заданного клиента>/overlapping/
```

![](assets/lab3/guests_overlapping.png)

Принять на работу сотрудника

```
POST /hotel/employees/
```

![](assets/lab3/employee_create.png)

Изменить информацию о сотруднике (уволить)

```
PUT /hotel/employees/<id сотрудника>/
```

![](assets/lab3/employee_update.png)

Создать расписание для сотрудника

```
POST /hotel/employees/<id сотрудника>/schedule/
```

![](assets/lab3/schedule_create.png)

Сбросить расписание сотрудника

```
DELETE /hotel/employees/<int:pk>/schedule/reset/
```

![](assets/lab3/schedule_reset.png)

Внести информацию о клиенте

```
POST /hotel/guests/
```

![](assets/lab3/guest_create.png)

Поселить клиента в номер

```
POST /hotel/rooms/<id номера>/booking/
```

![](assets/lab3/booking_create.png)

Освободить номер (выселить проживающего в данный момент клиента)

```
DELETE /hotel/rooms/<id номера, который нужно освободить>/booking/
```

![](assets/lab3/booking_delete.png)

Сформировать отчет за квартал текущего года, содежащий:

1. число клиентов за указанный период в каждом номере;
2. количество номеров не каждом этаже;
3. общая сумма дохода за каждый номер;
4. суммарный доход по всей гостинице.

```
GET /hotel/reports/<номер квартала от 1 до 4 включительно>/
```

![](assets/lab3/reports.png)

## **Подключение Djoser**

Регистрация

```
POST /auth/users/
```

![](assets/lab3/sign-up.png)

Получение токена

```
POST /auth/token/login/
```

![](assets/lab3/sign-in.png)

Получение информации о текущем пользователе

```
GET /auth/users/me/
```

![](assets/lab3/get_user.png)
