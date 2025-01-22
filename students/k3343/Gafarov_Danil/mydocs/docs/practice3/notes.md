# Практическое задание 3.1

## Django Web Framework. Запросы и их выполнение
---

### Задание

#### 1. Создание объектов

Воспользуйтесь проектом из практики 2.1. Напишите запросы для создания:
- 6–7 новых автовладельцев, 5–6 автомобилей.

Каждому автовладельцу необходимо назначить удостоверение и от 1 до 3 автомобилей. Задание можно выполнить в интерактивном режиме интерпретатора или в отдельном Python-файле. Результатом должны стать запросы и отображение созданных объектов.


#### 2. Написать запросы на фильтрацию  

- Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
- Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
- Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
- Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
- Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

#### 3. Написать запросы на агрегацию
- Вывод даты выдачи самого старшего водительского удостоверения
- Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
- Выведите количество машин для каждого водителя
- Подсчитайте количество машин каждой марки
- Отсортируйте всех автовладельцев по дате выдачи удостоверения 
---

### Создание объектов

#### 1. Создание автовладельцев

```python
from Cars.models import CarOwner, Car, DriverLicense, Ownership
from datetime import datetime

owner1 = CarOwner.objects.create(first_name="Иван", last_name="Иванов", birth_date=datetime(1980, 5, 17))
owner2 = CarOwner.objects.create(first_name="Петр", last_name="Петров", birth_date=datetime(1975, 8, 23))
owner3 = CarOwner.objects.create(first_name="Сергей", last_name="Сергеев", birth_date=datetime(1990, 12, 5))
owner4 = CarOwner.objects.create(first_name="Алексей", last_name="Алексеев", birth_date=datetime(1985, 3, 14))
owner5 = CarOwner.objects.create(first_name="Михаил", last_name="Михайлов", birth_date=datetime(1995, 7, 29))
owner6 = CarOwner.objects.create(first_name="Дмитрий", last_name="Дмитриев", birth_date=datetime(1988, 9, 9))
owner7 = CarOwner.objects.create(first_name="Николай", last_name="Николаев", birth_date=datetime(1992, 11, 11))
```


#### 2. Создание автомобилей

```python
car1 = Car.objects.create(license_plate="A123BC77", brand="Toyota", model="Camry", color="Черный")
car2 = Car.objects.create(license_plate="B456CD99", brand="Honda", model="Civic", color="Белый")
car3 = Car.objects.create(license_plate="C789DE88", brand="Ford", model="Focus", color="Синий")
car4 = Car.objects.create(license_plate="D012EF66", brand="BMW", model="X5", color="Серый")
car5 = Car.objects.create(license_plate="E345FG55", brand="Audi", model="A6", color="Красный")
car6 = Car.objects.create(license_plate="F678GH44", brand="Mercedes", model="E200", color="Зеленый")
```

#### 3. Создание удостоверений

```python
license1 = DriverLicense.objects.create(
    car_owner=owner1,
    license_number="770001",
    license_type="B",
    issue_date=datetime(2000, 6, 15)
)
license2 = DriverLicense.objects.create(
    car_owner=owner2,
    license_number="770002",
    license_type="B",
    issue_date=datetime(1998, 9, 20)
)
license3 = DriverLicense.objects.create(
    car_owner=owner3,
    license_number="770003",
    license_type="B",
    issue_date=datetime(2010, 1, 5)
)
license4 = DriverLicense.objects.create(
    car_owner=owner4,
    license_number="770004",
    license_type="B",
    issue_date=datetime(2005, 4, 25)
)
license5 = DriverLicense.objects.create(
    car_owner=owner5,
    license_number="770005",
    license_type="B",
    issue_date=datetime(2015, 7, 30)
)
license6 = DriverLicense.objects.create(
    car_owner=owner6,
    license_number="770006",
    license_type="B",
    issue_date=datetime(2008, 11, 12)
)
license7 = DriverLicense.objects.create(
    car_owner=owner7,
    license_number="770007",
    license_type="B",
    issue_date=datetime(2012, 3, 18)
)
```

#### 4. Создание записей о владении

```python
Ownership.objects.create(
    car_owner=owner1,
    car=car1,
    start_date=datetime(2020, 1, 1),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner1,
    car=car2,
    start_date=datetime(2021, 5, 10),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner2,
    car=car2,
    start_date=datetime(2019, 3, 15),
    end_date=datetime(2021, 5, 9)
)
Ownership.objects.create(
    car_owner=owner2,
    car=car3,
    start_date=datetime(2020, 7, 22),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner3,
    car=car4,
    start_date=datetime(2018, 12, 1),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner4,
    car=car5,
    start_date=datetime(2017, 6, 18),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner4,
    car=car6,
    start_date=datetime(2019, 8, 25),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner4,
    car=car1,
    start_date=datetime(2016, 2, 10),
    end_date=datetime(2020, 1, 1)
)
Ownership.objects.create(
    car_owner=owner5,
    car=car3,
    start_date=datetime(2021, 9, 5),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner6,
    car=car6,
    start_date=datetime(2020, 10, 30),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner7,
    car=car5,
    start_date=datetime(2022, 2, 14),
    end_date=None
)
Ownership.objects.create(
    car_owner=owner7,
    car=car4,
    start_date=datetime(2023, 4, 20),
    end_date=None
)
```
#### 5. Вывод данных
```python
owners = CarOwner.objects.all()
for owner in owners:
    print(f"Владелец: {owner.first_name} {owner.last_name}, Дата рождения: {owner.birth_date.date()}")
    # Удостоверение
    try:
        license = DriverLicense.objects.get(car_owner=owner)
        print(f"  Удостоверение №{license.license_number}, Категория: {license.license_type}, Дата выдачи: {license.issue_date.date()}")
    except DriverLicense.DoesNotExist:
        print("  Удостоверение не найдено.")
    # Автомобили
    ownerships = Ownership.objects.filter(car_owner=owner)
    if ownerships.exists():
        print("  Автомобили:")
        for ownership in ownerships:
            car = ownership.car
            print(f"    {car.brand} {car.model}, Номер: {car.license_plate}, Цвет: {car.color}")
    else:
        print("  Автомобили не найдены.")
    print("-" * 40)
```
`Output:`
Владелец: Иван Иванов, Дата рождения: 1980-05-17
  Удостоверение №770001, Категория: B, Дата выдачи: 2000-06-15
  Автомобили:
    Toyota Camry, Номер: A123BC77, Цвет: Черный
    Honda Civic, Номер: B456CD99, Цвет: Белый
----------------------------------------
Владелец: Петр Петров, Дата рождения: 1975-08-23
  Удостоверение №770002, Категория: B, Дата выдачи: 1998-09-20
  Автомобили:
    Honda Civic, Номер: B456CD99, Цвет: Белый
    Ford Focus, Номер: C789DE88, Цвет: Синий
----------------------------------------
Владелец: Сергей Сергеев, Дата рождения: 1990-12-05
  Удостоверение №770003, Категория: B, Дата выдачи: 2010-01-05
  Автомобили:
    BMW X5, Номер: D012EF66, Цвет: Серый
----------------------------------------
Владелец: Алексей Алексеев, Дата рождения: 1985-03-14
  Удостоверение №770004, Категория: B, Дата выдачи: 2005-04-25
  Автомобили:
    Audi A6, Номер: E345FG55, Цвет: Красный
    Mercedes E200, Номер: F678GH44, Цвет: Зеленый
    Toyota Camry, Номер: A123BC77, Цвет: Черный
----------------------------------------
Владелец: Михаил Михайлов, Дата рождения: 1995-07-29
  Удостоверение №770005, Категория: B, Дата выдачи: 2015-07-30
  Автомобили:
    Ford Focus, Номер: C789DE88, Цвет: Синий
----------------------------------------
Владелец: Дмитрий Дмитриев, Дата рождения: 1988-09-09
  Удостоверение №770006, Категория: B, Дата выдачи: 2008-11-12
  Автомобили:
    Mercedes E200, Номер: F678GH44, Цвет: Зеленый
----------------------------------------
Владелец: Николай Николаев, Дата рождения: 1992-11-11
  Удостоверение №770007, Категория: B, Дата выдачи: 2012-03-18
  Автомобили:
    Audi A6, Номер: E345FG55, Цвет: Красный
    BMW X5, Номер: D012EF66, Цвет: Серый
----------------------------------------



### Написание запросов на фильтрацию

#### 1. Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
```python
toyota_cars = Car.objects.filter(brand="Toyota")
for car in toyota_cars:
    print(car)
```
`Output:`
Toyota Camry (A123BC77).

#### 2. Найти всех водителей с именем “Иван”
```python
owners_named_ivan = CarOwner.objects.filter(first_name="Иван")
for owner in owners_named_ivan:
    print(owner)
```
`Output:`
Иван Иванов.
#### 3. Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
```python
owner = CarOwner.objects.order_by('?').first()
owner_id = owner.id
driver_license = DriverLicense.objects.get(car_owner__id=owner_id)
print(driver_license)
```
`Output:`
Удостоверение №770001 (Иван Иванов).
#### 4. Вывести всех владельцев красных машин
```python
owners_with_red_cars = CarOwner.objects.filter(
    ownerships__car__color="Красный"
).distinct()
for owner in owners_with_red_cars:
    print(owner)
```
`Output:`
Алексей Алексеев, Николай Николаев.
#### 5. Найти всех владельцев, чей год владения машиной начинается с 2020

```python
owners_since_2020 = CarOwner.objects.filter(
    ownerships__start_date__year=2020
).distinct()
for owner in owners_since_2020:
    print(owner)
```
`Output:`
Иван Иванов, Петр Петров, Дмитрий Дмитриев.
### Демонстрация работы с агрегатами, аннотациями, группировками и сортировками.

#### 1. Вывод даты выдачи самого старшего водительского удостоверения
Для этого мы можем использовать метод aggregate() для нахождения минимальной даты из всех удостоверений.
```python
oldest_license_date = DriverLicense.objects.aggregate(oldest_issue_date=Min('issue_date'))
print(f"Дата выдачи самого старшего удостоверения: {oldest_license_date['oldest_issue_date'].date()}")
``` 
`Output:`
Дата выдачи самого старшего удостоверения: 1998-09-20
#### 2. Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
Здесь мы можем воспользоваться методом aggregate() для поиска самой поздней даты начала владения машины.
```python
latest_ownership_date = Ownership.objects.aggregate(latest_start_date=Max('start_date'))
print(f"Самая поздняя дата начала владения машиной: {latest_ownership_date['latest_start_date'].date()}")
``` 
`Output:`
Самая поздняя дата начала владения машиной: 2024-10-19
#### 3. Выведите количество машин для каждого водителя

Для подсчета количества машин, принадлежащих каждому водителю, можно использовать annotate() с функцией Count.

```python
owners_car_count = CarOwner.objects.annotate(car_count=Count('ownerships__car', distinct=True))
for owner in owners_car_count:
    print(f"{owner.first_name} {owner.last_name} владеет {owner.car_count} машинами")
``` 
`Output:`
Иван Иванов владеет 2 машинами

Петр Петров владеет 2 машинами

Сергей Сергеев владеет 1 машинами

Алексей Алексеев владеет 3 машинами

Михаил Михайлов владеет 1 машинами

Дмитрий Дмитриев владеет 1 машинами

Николай Николаев владеет 2 машинами

#### 4. Подсчитайте количество машин каждой марки

Для подсчета машин по маркам можно использовать values() с группировкой по марке и annotate() для подсчета

```python
brand_car_count = Car.objects.values('brand').annotate(count=Count('id'))
for item in brand_car_count:
    print(f"Марка {item['brand']} имеет {item['count']} машин")
``` 
`Output:`
Марка Audi имеет 1 машин

Марка BMW имеет 1 машин

Марка Ford имеет 1 машин

Марка Honda имеет 1 машин

Марка Mercedes имеет 1 машин

Марка Toyota имеет 1 машин
#### 5. Отсортируйте всех автовладельцев по дате выдачи удостоверения 

```python
owners_with_license = CarOwner.objects.filter(driver_license__isnull=False).distinct().order_by('driver_license__issue_date')
for owner in owners_with_license:
    license_issue_date = owner.driver_license.first().issue_date.date()
    print(f"{owner.first_name} {owner.last_name}, дата выдачи удостоверения: {license_issue_date}")
``` 
`Output:`
Петр Петров, дата выдачи удостоверения: 1998-09-20

Иван Иванов, дата выдачи удостоверения: 2000-06-15

Алексей Алексеев, дата выдачи удостоверения: 2005-04-25

Дмитрий Дмитриев, дата выдачи удостоверения: 2008-11-12

Сергей Сергеев, дата выдачи удостоверения: 2010-01-05

Николай Николаев, дата выдачи удостоверения: 2012-03-18

Михаил Михайлов, дата выдачи удостоверения: 2015-07-30