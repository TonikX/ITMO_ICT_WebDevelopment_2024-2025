# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов
### Club
#### Alpinists
1 **Получить список альпинистов**
```
GET /club/alpinists
```

2 **Добавить альпиниста**

```
POST /club/alpinists
```
3 **Получить список альпинистов, совершавших восхождение в заданный период**
```
GET /club/alpinists/ascendings_period
```
4 **Получить список альпинистов с их количеством восхождений на каждую гору**
```
GET /club/alpinists/mountain_ascendings
```
5 **Получить подробную информацию об альпинисте**
```
GET /club/alpinists/{id}
```
6 **Изменить данные альпиниста**
```
PUT /club/alpinists/{id}{employee_id}/update
```
7 **Изменить данные альпиниста**
```
PATCH /club/alpinists/{id}/{employee_id}/update
```
#### Ascendings
8 **Получить список восхождений**
```
GET /club/ascendings
```
9 **Добавить восхождение**
```
POST  /club/ascendings
```
10 **Получить информацию о восхождении**
```
GET /club/ascendings/{id}
```
11 **Изменить информацию о восхождении**
```
PUT /club/ascendings/{id}/update
```
11 **Изменить информацию о восхождении**
```
PATCH /club/ascendings/{id}/update
```
#### Ascending Group
13 **Получить список групп**
```
GET /club/ascengings/groups
```
14 **Добавить группу**
```
POST /club/ascengings/groups
```
15 **Получить подробную информацию о группе**
```
GET /club/ascengings/groups/{id}
```
16 **Изменить информацию о группе**
```
PUT /club/ascengings/groups/{id}/update
```
17 **Изменить информацию о группе**
```
PATCH /club/ascengings/groups/{id}/update
```
#### Alpinist in group
18 **Получить информацию об участниках определённной группы**
```
GET /club/ascengings/groups/{group_id}/members
```
19 **Добавить участника в определённую группу**
```
POST /club/ascengings/groups/{group_id}/members
```
20 **Получить информацию об участнике группы**
```
GET /club/ascengings/groups/members/{id}
```
21 **Изменить информацию об участнике группы**
```
PUT /club/ascengings/groups/members/{id}/update
```
22 **Изменить информацию об участнике группы**
```
PATCH /club/ascengings/groups/members/{id}/update
```
#### Clubs
23 **Получить информацию клубах**
```
GET /club/clubs
```
#### Mountains
24 **Получить список вершин**
```
GET /club/mountains
```
25 **Добавить вершину**
```
POST /club/mountains
```
26 **Получить информацию об определённой вершине**
```
GET /club/mountains/{id}
```
27 **Изменить информацию о вершине**
```
PUT /club/mountains/{id}/update
```
28 **Изменить информацию о вершине**
```
PATCH /club/mountains/{id}/update
```
29 **Получить список вершин с количеством альпинистов, которые были на них**
```
GET /club/mountains/alpinists_count
```
30 **Получить список вершин, на которых не было восхождений**
```
GET /club/mountains/without_ascendings
```
#### Report
31 **Получить отчёт о восхождениях в заданный период**
```
GET /club/report
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


