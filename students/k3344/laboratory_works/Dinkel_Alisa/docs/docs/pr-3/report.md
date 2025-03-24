# Отчет по практической работе №3

## Практическая работа 3.1

### Запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей

```python
owners = [
    CarOwner.objects.create(last_name="Смирнов", first_name="Андрей", birth_date="1985-03-15"),
    CarOwner.objects.create(last_name="Петров", first_name="Алексей", birth_date="1992-07-21"),
    CarOwner.objects.create(last_name="Сидорова", first_name="Мария", birth_date="1998-11-05"),
    CarOwner.objects.create(last_name="Васильев", first_name="Олег", birth_date="1990-05-30"),
    CarOwner.objects.create(last_name="Фёдорова", first_name="Елена", birth_date="2001-09-14"),
    CarOwner.objects.create(last_name="Григорьев", first_name="Дмитрий", birth_date="1995-12-22"),
]

cars = [
    Car.objects.create(license_plate="XYZ001", brand="Honda", model="Civic", color="Красный"),
    Car.objects.create(license_plate="XYZ002", brand="Ford", model="Focus", color="Серый"),
    Car.objects.create(license_plate="XYZ003", brand="Hyundai", model="Tucson", color="Белый"),
    Car.objects.create(license_plate="XYZ004", brand="Kia", model="Sportage", color="Черный"),
    Car.objects.create(license_plate="XYZ005", brand="Volkswagen", model="Polo", color="Синий"),
    Car.objects.create(license_plate="XYZ006", brand="Nissan", model="X-Trail", color="Зеленый"),
]
```

### Каждому автовладельцу назначьте удостоверение
```python
licenses = [
    DriverLicense.objects.create(owner=owners[0], license_number="A123456789", license_type="B", issue_date=date(2020, 5, 10)),
    DriverLicense.objects.create(owner=owners[1], license_number="B987654321", license_type="B", issue_date=date(2018, 3, 22)),
    DriverLicense.objects.create(owner=owners[2], license_number="C456123789", license_type="B", issue_date=date(2021, 7, 19)),
    DriverLicense.objects.create(owner=owners[3], license_number="D654789321", license_type="B", issue_date=date(2019, 11, 5)),
    DriverLicense.objects.create(owner=owners[4], license_number="E321987654", license_type="B", issue_date=date(2022, 2, 28)),
    DriverLicense.objects.create(owner=owners[5], license_number="F789123456", license_type="B", issue_date=date(2017, 9, 14)),
]
```

### Каждому автовладельцу назначьте от 1 до 3 автомобилей
```python
Ownership.objects.create(owner=owners[0], car=cars[0], start_date="2023-06-01")
Ownership.objects.create(owner=owners[0], car=cars[1], start_date="2024-02-10")

Ownership.objects.create(owner=owners[1], car=cars[2], start_date="2022-08-15")
Ownership.objects.create(owner=owners[1], car=cars[3], start_date="2023-05-01", end_date="2024-01-31")

Ownership.objects.create(owner=owners[2], car=cars[4], start_date="2023-03-10")
Ownership.objects.create(owner=owners[2], car=cars[5], start_date="2024-01-15")

Ownership.objects.create(owner=owners[3], car=cars[0], start_date="2021-09-20", end_date="2023-05-30")
Ownership.objects.create(owner=owners[3], car=cars[2], start_date="2024-02-01")

Ownership.objects.create(owner=owners[4], car=cars[3], start_date="2023-07-01")
Ownership.objects.create(owner=owners[4], car=cars[5], start_date="2024-03-01")

Ownership.objects.create(owner=owners[5], car=cars[1], start_date="2020-05-10", end_date="2022-04-15")
Ownership.objects.create(owner=owners[5], car=cars[4], start_date="2023-10-12")
```
### Выведите все машины марки “Toyota” (или любой другой марки, которая у вас есть)

```python
Car.objects.filter(brand="Toyota")
```

### Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)

```python
CarOwner.objects.filter(first_name="Олег")
```

### Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)

```python
import random

random_owner_id = random.choice(CarOwner.objects.all()).id_owner
DriverLicense.objects.get(owner__id_owner=random_owner_id)
```

### Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)

```python
CarOwner.objects.filter(ownerships__car__color="Красный").distinct()
```

### Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

```python
CarOwner.objects.filter(ownerships__start_date__year=2023).distinct()

```

### Вывод даты выдачи самого старшего водительского удостоверения

```python
DriverLicense.objects.aggregate(Min('issue_date'))
```

### Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе

```python
Ownership.objects.aggregate(Max('end_date'))
```

### Выведите количество машин для каждого водителя

```python
CarOwner.objects.annotate(num_cars=Count('ownerships')).values('id_owner', 'num_cars')
```

### Подсчитайте количество машин каждой марки

```python
Car.objects.values('brand').annotate(num_cars=Count('id_car'))
```

### Отсортируйте всех автовладельцев по дате выдачи удостоверения

```python
CarOwner.objects.order_by('license__issue_date').distinct()
```

## Практическая работа 3.2
Реализовать ендпоинты для добавления и просмотра скилов методом, описанным в пункте выше.

### Добавление скилов

POST /war/skills/

```json
{
    "title": "Защита щитом"
}
```
```json
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 10,
    "title": "Защита щитом"
}
```

### Просмотр скилов

GET /war/skills/

```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "Skills": [
        {
            "id": 1,
            "title": "skill_1"
        },
        {
            "id": 2,
            "title": "skill_2"
        },
        {
            "id": 3,
            "title": "skill_2"
        },
        {
            "id": 4,
            "title": "skill_1"
        },
        {
            "id": 5,
            "title": "skill_5"
        },
        {
            "id": 6,
            "title": "random skill"
        },
        {
            "id": 7,
            "title": "Атака мечом"
        },
        {
            "id": 8,
            "title": "Огненный шар"
        },
        {
            "id": 9,
            "title": "Скрытность"
        },
        {
            "id": 10,
            "title": "Защита щитом"
        }
    ]
}
```
### Вывод полной информации о всех войнах и их профессиях
GET /war/warriors/professions/
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "Русский язык",
        "race": "s",
        "level": 11,
        "profession": {
            "id": 1,
            "title": "prof_1",
            "description": "111"
        }
    },
    {
        "id": 2,
        "name": "Обществознание",
        "race": "d",
        "level": 8,
        "profession": {
            "id": 2,
            "title": "prof_2",
            "description": "prof_2"
        }
    },
    {
        "id": 3,
        "name": "Русский язык",
        "race": "d",
        "level": 1,
        "profession": {
            "id": 1,
            "title": "prof_1",
            "description": "111"
        }
    },
    {
        "id": 4,
        "name": "Алекс",
        "race": "s",
        "level": 5,
        "profession": {
            "id": 3,
            "title": "Воин",
            "description": "Мастер меча"
        }
    },
    {
        "id": 5,
        "name": "Мерлин",
        "race": "d",
        "level": 10,
        "profession": {
            "id": 4,
            "title": "Маг",
            "description": "Использует магию"
        }
    },
    {
        "id": 6,
        "name": "Тень",
        "race": "t",
        "level": 7,
        "profession": {
            "id": 5,
            "title": "Разбойник",
            "description": "Специалист по скрытности"
        }
    }
]
```
### Вывод полной информации о всех войнах и их скиллах
GET /war/warriors/skills/
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "name": "Русский язык",
        "race": "s",
        "level": 11,
        "skill": []
    },
    {
        "id": 2,
        "name": "Обществознание",
        "race": "d",
        "level": 8,
        "skill": []
    },
    {
        "id": 3,
        "name": "Русский язык",
        "race": "d",
        "level": 1,
        "skill": []
    },
    {
        "id": 4,
        "name": "Алекс",
        "race": "s",
        "level": 5,
        "skill": [
            {
                "id": 7,
                "title": "Атака мечом"
            }
        ]
    },
    {
        "id": 5,
        "name": "Мерлин",
        "race": "d",
        "level": 10,
        "skill": [
            {
                "id": 8,
                "title": "Огненный шар"
            }
        ]
    },
    {
        "id": 6,
        "name": "Тень",
        "race": "t",
        "level": 7,
        "skill": [
            {
                "id": 9,
                "title": "Скрытность"
            }
        ]
    }
]
```
### Вывод полной информации о войне (по id), его профессиях и скилах.
GET /war/warriors/6/
```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 6,
    "profession": {
        "id": 5,
        "title": "Разбойник",
        "description": "Специалист по скрытности"
    },
    "skill": [
        {
            "id": 9,
            "title": "Скрытность"
        }
    ],
    "race": "t",
    "name": "Тень",
    "level": 7
}
```
### Удаление война по id
DELETE /war/warriors/1/
```json
GET /war/warriors/1/
HTTP 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "No Warrior matches the given query."
}
```
### Редактирование информации о войне
PATCH /war/warriors/6/
```json
{
    "level": 10
}
```
```json
{
    "id": 6,
    "profession": {
        "id": 5,
        "title": "Разбойник",
        "description": "Специалист по скрытности"
    },
    "skill": [
        {
            "id": 9,
            "title": "Скрытность"
        }
    ],
    "race": "t",
    "name": "Тень",
    "level": 10
}
```