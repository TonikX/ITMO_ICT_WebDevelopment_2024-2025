# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов
### Hotel
#### Clients
1 **Получить список клиентов**
```
GET /hotel/clients
```

2 **Добавить клиента**

```
POST /hotel/clients
```
3 **Получить количество клиентов, прибывших из заданного города**
```
GET /hotel/clients/city
```

#### EmployeesSchedule
4 **Получить список расписаний работников**
```
GET /hotel/employees/schedule
```
5 **Добавить список расписаний работников**
```
POST /hotel/employees/schedule
```
6 **Изменить расписание сотрудника**
```
PUT /hotel/employees/schedule/{employee_id}/update
```
7 **Изменить расписание сотрудника**
```
PATCH /hotel/employees/schedule/{employee_id}/update
```
8 **Получить сотрудника, который убирал номер определённого клиента в определённый день недели**
```
PUT /hotel/employees/schedule_client
```
#### Employees
9 **Получить список сотрудников**
```
GET /hotel/employees
```
10 **Добавить сотрудников**
```
POST /hotel/employees
```
11 **Получить подробную информацию о сотруднике**
```
GET /hotel/employees/{id}
```
12 **Удалить сотрудника**
```
DELETE /hotel/employees/{id}
```
#### Reservations
13 **Получить список резервирований**
```
GET /hotel/reservations
```
14 **Добавить резервирование**
```
POST /hotel/reservations
```
15 **Получить подробную информацию о резервировании**
```
GET /hotel/reservations/{id}
```
16 **Удалить резервирование**
```
DELETE /hotel/reservations/{id}
```
17 **Получить информацию о клиентах, проживавших в те же дни, что и определённый клиент, в определённый период**
```
GET /hotel/reservations/client_period
```
18 **Получить информацию о клиентах, проживавших в комнате в определённый период**
```
GET /hotel/reservations/room_period
```
#### Rooms
19 **Получить список комнат**
```
GET /hotel/rooms
```
20 **Получить количество свободных комнат**
```
GET /hotel/rooms/free
```
21 **Получить информацию о комнате**
```
GET /hotel/rooms/{id}
```
### Auth
22 **Получить токен юзера по паролю и никнейму**
```
POST /auth/token/login
```
23 **Вывести информацию о пользователе**
```
GET /auth/users/me
```
24 **Зарегистрировать пользователя**
```
POST /auth/users
```


