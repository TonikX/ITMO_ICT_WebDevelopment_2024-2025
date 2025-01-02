# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов
### Manufactory
#### Breeds
1 **Получить список пород**
```
GET /manufactory/breeds/
```

2 **Добавить породу**

```
POST /manufactory/breeds/
```
3 **Получить разницу между средним значением производительности породы и средним числом по цеху**
```
GET /manufactory/breeds/difference/
```

4 **Получить детальную информацию о породе**
```
GET /manufactory/breeds/{id}
```
5 **Изменить породу**
```
UPDATE /manufactory/breeds/{id}
```
6 **Изменить породу**
```
PATCH /manufactory/breeds/{id}
```
7 **Удалить породу**
```
DELETE /manufactory/breeds/{id}
```

#### Cells
8 **Получить список клеток**
```
GET /manufactory/cells/
```

9 **Добавить клетку**
```
POST /manufactory/cells/
```

#### Chicken
10 **Получить список куриц**
```
GET /manufactory/chicken/

```
11 **Добавить курицу**
```
POST /manufactory/chicken/
```
12 **Удалить курицу**
```
DELETE /manufactory/chicken/{id}
```

13 **Получить информацию о курице**
```
GET /manufactory/chicken/{id}
```
14 **Изменить информацию о курице**
```
UPDATE /manufactory/chicken/{id}
```
15 **Изменить информацию о курице**
```
PATCH /manufactory/chicken/{id}
```

#### Diets
16 **Получить список диет**
```
GET /manufactory/diets/
```
17 **Добавить диету**
```
POST /manufactory/diets/
```
18 **Получить информацию о диете**
```
GET /manufactory/diets/{id}
```

19 **Изменить информацию о диете**
```
UPDATE /manufactory/diets/{id}
```
20 **Изменить информацию о диете**
```
PATCH /manufactory/diets/{id}
```
21 **Удалить диету**
```
DELETE /manufactory/diets/{id}
```
22 **Производительность по породам**
```
GET /manufactory/egg/performance/breed/
```

#### Employees
23 GET/POST
```
METHOD /manufactory/employees
```

24 CRUD

```
METHOD /manufactory/employees/{id}
```


#### Responsible Employees CRUD's

25 GET/POST
```
METHOD /manufactory/employees/cells
```

26 CRUD
```
METHOD /manufactory/employees/cells/{id}
```

#### Employees contracts CRUD's
27 GET/POST
```
METHOD /manufactory/employees/contracts/{id}
```

28 CRUD
```
METHOD /manufactory/employees/contracts/{id}
``` 

29 Получить отчёт за прошедший месяц
```
GET /manufactory/reports
```

30 В каком цехе наибольшее количество птиц определённой породы
```
GET /manufactory/workshop/breeds
```

31 Количество кур каждой породы в каждом цехе
```
GET /manufactory/workshop/breeds/count
```

### Auth
32 **Получить токен юзера по паролю и никнейму**
```
POST /auth/token/login
```
33 **Вывести информацию о пользователе**
```
GET /auth/users/me
```
34 **Зарегистрировать пользователя**
```
POST /auth/users
```

