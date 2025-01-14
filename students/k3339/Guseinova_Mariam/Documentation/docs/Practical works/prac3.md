# Практическая работа 3. Simple DRF project.
За основу взят проект из практики 2.1.

## Практическое задание 1: 
Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. 

```python
from project_first_app.models import User, Car, Ownership, DriverLicense
from datetime import date

owner_1 = User.objects.create_user(username="Natalia", password="0000", passport_number="11111111")
owner_2 = User.objects.create_user(username="Mariam", password="0000", passport_number="22222")
owner_3 = User.objects.create_user(username="Inga", password="0000", passport_number="333333")
owner_4 = User.objects.create_user(username="Anna", password="0000", passport_number="444444")
owner_5 = User.objects.create_user(username="Maria", password="0000", passport_number="5555555")
owner_6 = User.objects.create_user(username="Ivan", password="0000", passport_number="6666666")

car_1 = Car.objects.create(brand="Ferrari", model="model", color="Red", state_number="AA123eee")
car_2 = Car.objects.create(brand="Toyota", model="model", color="Green", state_number="BB345eee")
car_3 = Car.objects.create(brand="Jaguar", model="model", color="White", state_number="CC678eee")
car_4 = Car.objects.create(brand="Toyota", model="model", color="Black", state_number="DD901eee")
car_5 = Car.objects.create(brand="KIA", model="model", color="Rose", state_number="EE234eee")

license_1 = DriverLicense.objects.create(owner=owner_1, license_number="32563", type="A", date_of_getting=date(2014, 5, 1))
license_2 = DriverLicense.objects.create(owner=owner_2, license_number="2332", type="A", date_of_getting=date(2016, 7, 2))
license_3 = DriverLicense.objects.create(owner=owner_3, license_number="3663", type="B", date_of_getting=date(2017, 8, 3))
license_4 = DriverLicense.objects.create(owner=owner_4, license_number="38283", type="B", date_of_getting=date(2018, 9, 4))
license_5 = DriverLicense.objects.create(owner=owner_5, license_number="3333", type="C", date_of_getting=date(2019, 10, 5))
license_6 = DriverLicense.objects.create(owner=owner_6, license_number="36273", type="C", date_of_getting=date(2020, 11, 6))

Ownership.objects.create(owner=owner_1, car=car_1, start_date=date(2024, 1, 1))
Ownership.objects.create(owner=owner_1, car=car_2, start_date=date(2024, 1, 15))
Ownership.objects.create(owner=owner_2, car=car_3, start_date=date(2024, 2, 1))
Ownership.objects.create(owner=owner_3, car=car_4, start_date=date(2024, 3, 1))
Ownership.objects.create(owner=owner_4, car=car_5, start_date=date(2024, 4, 1))
Ownership.objects.create(owner=owner_5, car=car_2, start_date=date(2024, 5, 1))
Ownership.objects.create(owner=owner_6, car=car_3, start_date=date(2024, 6, 1))
Ownership.objects.create(owner=owner_6, car=car_4, start_date=date(2024, 7, 1))
```
## Практическое задание 2: 

* Где это необходимо, добавьте related_name к полям модели
* Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
* Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
* Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
* Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
* Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

Все машины марки “Toyota”:
```python
toyota = Car.objects.filter(make="Toyota")
for car in toyota:
    print(car)
```
Вывод:
```python
Toyota model BB345eee
Toyota model DD901eee
```
Водители с именем Natalia:
```python
Natalia_ = User.objects.filter(username__icontains="Natalia")
for owner in Natalia_:
    print(owner)
```
Вывод:
```python
Natalia
```
Случайный владелец и его удостоверение:
```python
owner = User.objects.first()
print(f"User ID: {user.id}, Name: {user.username}")
license_obj = DriverLicense.objects.get(user_id=user.id)
print(f"License: {license_obj.license_number}, Type: {license_obj.type}")
```
Вывод:
```python
User ID: 1, Name: test
License: 12345, Type: A
```
Все владельцы красных машин:
```python
red_cars = Car.objects.filter(color="Red")
red_car_owners = User.objects.filter(ownerships__car__in=red_cars).distinct()
for owner in red_car_owners:
    print(owner)
```
Вывод:
```python
Natalia
```
Все владельцы, чей год владения машиной начинается с 2024:
```python
owners_of_2024 =User.objects.filter(ownerships__start_date__year=2024).distinct()
for owner in owners_from_2024:
    print(owner)
```
Вывод:
```python
Natalia
Mariam
Inga
Anna
Maria
Ivan
```
## Практическое задание 3: 
Необходимо реализовать следующие запросы c применением описанных методов:
* Вывод даты выдачи самого старшего водительского удостоверения
* Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
* Выведите количество машин для каждого водителя
* Подсчитайте количество машин каждой марки
* Отсортируйте всех автовладельцев по дате выдачи удостоверения

Самое старое водительское удостоверение:
```python
oldest_license_date = DriverLicense.objects.aggregate(oldest_date=Min("date_of_getting"))
print(f"Самая ранняя дата получения удостоверения: {oldest_license_date['oldest_date']}")
```
Вывод:
```python
Самая ранняя дата выдачи удостоверения: 2014-05-01
```

Самая поздняя дата владения машиной:
```python
latest_start_date = Ownership.objects.aggregate(latest_start_date=Max("start_date"))
print(f"Самая поздняя дата начала владения машиной: {latest_start_date['latest_start_date']}")
```
Вывод:
```python
Самая поздняя дата начала владения машиной: 2024-07-01
```
Количество машин для каждого водителя:
```python
user_cars_count = User.objects.annotate(car_count=Count("ownerships__car")).distinct()
for user in user_cars_count:
    print(f"{user.username} владеет {user.car_count} машин(ой/ами)")
```
Вывод:
```python
Natalia владеет 2 машин(ой/ами)
Mariam владеет 1 машин(ой/ами)
Inga владеет 1 машин(ой/ами)
Anna владеет 1 машин(ой/ами)
Maria владеет 1 машин(ой/ами)
Ivan владеет 2 машин(ой/ами)
```
Количество машин каждой марки:
```python
car_brand_counts = Car.objects.values('brand').annotate(count=Count('brand'))
for brand_count in car_brand_counts:
    print(f"{brand_count['brand']}: {brand_count['count']} cars")
```
Вывод:
```python
Ferrari: 1 cars
Toyota: 2 cars
Jaguar: 1 cars
KIA: 1 cars
```
Все автовладельцев по дате выдачи удостоверения:
```python
owners_sorted_by_license = User.objects.order_by("licenses__date_of_issue").distinct()
for owner in owners_sorted_by_license:
    license_obj = User.licenses.first()
    print(f"{user.username} - Дата выдачи удостоверения: {license_obj.date_of_issue}")
```
Вывод:
```python
Natalia - Дата выдачи удостоверения: 2014-05-01
Mariam - Дата выдачи удостоверения: 2016-07-02
Inga - Дата выдачи удостоверения: 2017-08-03
Anna - Дата выдачи удостоверения: 2018-09-04
Maria - Дата выдачи удостоверения: 2019-10-05
Ivan - Дата выдачи удостоверения: 2020-11-06
```
