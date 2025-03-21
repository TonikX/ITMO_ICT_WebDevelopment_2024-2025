# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов
### School
#### Schedule
1 **Получить расписание**
```
GET /school/schedules
```
![img.png](images/img.png)
2 **Добавить расписание**

```
POST /school/schedules
```
![img_1.png](images/img_1.png)

3 **Получить определённое расписание**
```
GET /school/schedules/{id}
```
![img_2.png](images/img_2.png)
4 **Удалить расписание**
```
DELETE /school/schedules/{id}/delete
```
5 **Изменить расписание**
```
UPDATE /school/schedules/{id}/update
```
6 **Изменить расписание**
```
PATCH  /school/schedules/{id}/update
```
7 **Получить предмет, который будет преподаваться в определённом классе, в определённый день недели, на определённом уроке.**
```
GET /school/schedule/subject
```
![img_3.png](images/img_3.png)
#### Students
8 **Получить список учеников**
```
GET /school/students
```
![img_4.png](images/img_4.png)
9 **Добавить ученика**
```
POST  /school/students
```
![img_5.png](images/img_5.png)
10 **Получить подробную информацию об ученике**
```
GET /school/students/{id}
```
![img_6.png](images/img_6.png)
11 **Удалить ученика**
```
DELETE /school/students/{id}/delete
```
![img_7.png](images/img_7.png)
12 **Изменить данные об ученике**
```
UPDATE /school/students/{id}/update
```
13 **Изменить данные об ученике**
```
PATCH /school/students/{id}/update
```
14 **Получить информацию о количестве мальчиков и девочек в каждом классе**
```
GET /school/students/gender
```
![img_8.png](images/img_8.png)
#### Teachers
15 **Получить список учителей**
```
GET /school/teachers
```
![img_9.png](images/img_9.png)
16 **Добавить учителя**
```
POST /school/teachers
```
![img_10.png](images/img_10.png)
17 **Удалить учителя**
```
DELETE /school/teachers/{id}/delete
```
18 **Получить подробную информацию об учителе**
```
GET /school/teachers/{id}
```
![img_11.png](images/img_11.png)
19 **Изменить данные об учителе**
```
UPDATE /school/teachers/{id}/update
```
20 **Изменить данные об учителе**
```
PATCH /school/teachers/{id}/update
```
21 **Получить список классных руководителей**
```
GET /school/teachers/home
```
![img_12.png](images/img_12.png)
22 **Добавить классного руководителя**
```
POST /school/teachers/home
```
![img_13.png](images/img_13.png)
23 **Получить список учителей, преподающих те же предметы, что и учитель, ведущий
информатику в заданном классе.**
```
GET /school/teachers/colleagues
```
![img_14.png](images/img_14.png)
#### Rooms
24  **Получить количество аудиторий для базовых и профильных дисциплин**
```
GET /school/rooms/profile_base
```
![img_15.png](images/img_15.png)
#### Subjects
25 **Получить список предметов и количество учителей, которые преподают дисциплину**
```
GET /school/subjects/teachers_count
```

#### Report
26 **Получить отчёт об определённом классе**
```
GET /school/report
```

### Auth
27 **Получить токен юзера по паролю и никнейму**
```
POST /auth/token/login
```
28 **Вывести информацию о пользователе**
```
GET /auth/users/me
```
29 **Зарегистрировать пользователя**
```
POST /auth/users
```

