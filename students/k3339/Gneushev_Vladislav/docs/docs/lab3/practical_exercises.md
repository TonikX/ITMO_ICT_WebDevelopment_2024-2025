## Практическая работа 3.1

### Задание 1
Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей.

Код:
```
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogfspo.settings')
django.setup()

from datetime import date
from blog.models import CarOwner, Car, Ownership, DriverLicense


owner1 = CarOwner.objects.create_user(username='johndoe', first_name='John', last_name='Doe', birth_date='1985-05-12')
owner2 = CarOwner.objects.create_user(username='janedoe', first_name='Jane', last_name='Doe', birth_date='1990-07-23')
owner3 = CarOwner.objects.create_user(username='robertsmith', first_name='Robert', last_name='Smith', birth_date='1978-11-01')
owner4 = CarOwner.objects.create_user(username='annajohnson', first_name='Anna', last_name='Johnson', birth_date='1983-04-15')
owner5 = CarOwner.objects.create_user(username='peterbrown', first_name='Peter', last_name='Brown', birth_date='1992-10-09')
owner6 = CarOwner.objects.create_user(username='williamj', first_name='William', last_name='Jenkins', birth_date='1955-10-09')

car1 = Car.objects.create(state_number='A123BC77', brand='Toyota', model='C', color='Black')
car2 = Car.objects.create(state_number='B456CD99', brand='BMW', model='X', color='White')
car3 = Car.objects.create(state_number='C789DE01', brand='Mercedes', model='E', color='Silver')
car4 = Car.objects.create(state_number='D012EF22', brand='Tesla', model='S', color='Blue')
car5 = Car.objects.create(state_number='E345FG33', brand='Ford', model='A', color='Red')
car6 = Car.objects.create(state_number='E59VAGH2', brand='Ford', model='B', color='Brown')

DriverLicense.objects.create(owner=owner1, number='DL123456', license_type='B', issued_at=date(2010, 5, 20))
DriverLicense.objects.create(owner=owner2, number='DL789012', license_type='C', issued_at=date(2015, 6, 15))
DriverLicense.objects.create(owner=owner3, number='DL345678', license_type='A', issued_at=date(2008, 3, 10))
DriverLicense.objects.create(owner=owner4, number='DL901234', license_type='D', issued_at=date(2012, 12, 5))
DriverLicense.objects.create(owner=owner5, number='DL567890', license_type='E', issued_at=date(2018, 9, 25))
DriverLicense.objects.create(owner=owner6, number='DL111122', license_type='Z', issued_at=date(2015, 9, 25))

Ownership.objects.create(owner=owner1, car=car1, start_date=date(2015, 1, 1))
Ownership.objects.create(owner=owner2, car=car2, start_date=date(2020, 6, 1))
Ownership.objects.create(owner=owner3, car=car3, start_date=date(2017, 3, 15))
Ownership.objects.create(owner=owner4, car=car4, start_date=date(2010, 8, 10))
Ownership.objects.create(owner=owner5, car=car5, start_date=date(2021, 7, 1))
Ownership.objects.create(owner=owner6, car=car6, start_date=date(2023, 5, 10))

for owner in CarOwner.objects.all():
    print(f'Owner: {owner}, license: {owner.driverlicense_set.first()}')
    for ownership in owner.ownerships.all():
        print(f'- Car: {ownership.car}, start date: {ownership.start_date}, end date: {ownership.end_date}')
```

Вывод в консоль:
```
Owner: John Doe, license: John Doe - DL123456 (B)
- Car: A123BC77 - Toyota C (Black), start date: 2015-01-01, end date: None
Owner: Jane Doe, license: Jane Doe - DL789012 (C)
- Car: B456CD99 - BMW X (White), start date: 2020-06-01, end date: None
Owner: Robert Smith, license: Robert Smith - DL345678 (A)
- Car: C789DE01 - Mercedes E (Silver), start date: 2017-03-15, end date: None
Owner: Anna Johnson, license: Anna Johnson - DL901234 (D)
- Car: D012EF22 - Tesla S (Blue), start date: 2010-08-10, end date: None
Owner: Peter Brown, license: Peter Brown - DL567890 (E)
- Car: E345FG33 - Ford A (Red), start date: 2021-07-01, end date: None
Owner: William Jenkins, license: William Jenkins - DL111122 (Z)
- Car: E59VAGH2 - Ford B (Brown), start date: 2023-05-10, end date: None
```


### Задание 2
По созданным данным написать следующие запросы на фильтрацию:

- Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
- Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
- Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
- Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
- Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

> Где это необходимо, добавьте related_name к полям модели

Код:
```
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogfspo.settings')
django.setup()

from blog.models import CarOwner, Car, DriverLicense, Ownership


# 1 запрос
toyota_cars = Car.objects.filter(brand="Toyota")
print("Все машины марки Toyota:")
for car in toyota_cars:
    print(f"- {car}")
print()


# 2 запрос
drivers_named_oleg = CarOwner.objects.filter(first_name="John")
print("Все водители с именем John:")
for driver in drivers_named_oleg:
    print(f"- {driver}")
print()


# 3 запрос
random_owner = CarOwner.objects.first()
owner_id = random_owner.id
print(f"Случайный владелец: {random_owner}, ID: {owner_id}")

driver_license = DriverLicense.objects.get(owner_id=owner_id)
print(f"Удостоверение владельца {owner_id}: {driver_license}")
print()


# 4 запрос
red_cars = Car.objects.filter(color="Red")
print("Владельцы красных машин:")
for car in red_cars:
    owners = car.owner.all()
    for owner in owners:
        print(f"- {owner}")
print()


# 5 запрос
owners_with_cars_from_2010 = Ownership.objects.filter(start_date__year=2010)
print("Владельцы, чей год владения машиной начинается с 2010:")
for ownership in owners_with_cars_from_2010:
    print(f"- {ownership.owner}")
```

Вывод в консоль:
```
Все машины марки Toyota:
- A123BC77 - Toyota C (Black)

Все водители с именем John:
- John Doe

Случайный владелец: John Doe, ID: 1
Удостоверение владельца 1: John Doe - DL123456 (B)

Владельцы красных машин:
- Peter Brown

Владельцы, чей год владения машиной начинается с 2010:
- Anna Johnson
```


### Задание 3
Необходимо реализовать следующие запросы c применением описанных методов:

- Вывод даты выдачи самого старшего водительского удостоверения
- Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
- Выведите количество машин для каждого водителя
- Подсчитайте количество машин каждой марки
- Отсортируйте всех автовладельцев по дате выдачи удостоверения

Код:
```
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogfspo.settings')
django.setup()

from blog.models import CarOwner, Car, DriverLicense, Ownership
from django.db.models import Count, Min, Max

# 1 запрос
oldest_license_date = DriverLicense.objects.order_by('issued_at').first().issued_at
print(f"Дата выдачи самого старшего водительского удостоверения: {oldest_license_date}")
print()


# 2 запрос
latest_end_date = Ownership.objects.aggregate(latest_date=Max("end_date"))["latest_date"]
print(f"Самая поздняя дата владения машиной: {latest_end_date}")
print()


# 3 запрос
drivers_with_car_count = CarOwner.objects.annotate(car_count=Count('ownerships'))
for driver in drivers_with_car_count:
    print(f"- Водитель: {driver}, машин: {driver.car_count}")
print()

# 4 запрос
cars_per_brand = Car.objects.values('brand').annotate(count=Count('id')).order_by('-count')
print("Количество машин каждой марки:")
for entry in cars_per_brand:
    print(f"- Марка: {entry['brand']}, машин: {entry['count']}")
print()

# 5 запрос
owners_sorted_by_license_date = (
    CarOwner.objects.annotate(earliest_license_date=Min('driverlicense__issued_at'))
    .order_by('earliest_license_date')
)
print("Владельцы, отсортированные по дате выдачи удостоверения:")
for owner in owners_sorted_by_license_date:
    print(f"- Владелец: {owner}, дата выдачи первого удостоверения: {owner.earliest_license_date}")
```

Вывод в консоль:
```
Дата выдачи самого старшего водительского удостоверения: 2008-03-10

Самая поздняя дата владения машиной: None

- Водитель: Anna Johnson, машин: 1
- Водитель: Jane Doe, машин: 1
- Водитель: John Doe, машин: 1
- Водитель: Peter Brown, машин: 1
- Водитель: Robert Smith, машин: 1
- Водитель: William Jenkins, машин: 1

Количество машин каждой марки:
- Марка: Ford, машин: 2
- Марка: Toyota, машин: 1
- Марка: Tesla, машин: 1
- Марка: Mercedes, машин: 1
- Марка: BMW, машин: 1

Владельцы, отсортированные по дате выдачи удостоверения:
- Владелец: Robert Smith, дата выдачи первого удостоверения: 2008-03-10
- Владелец: John Doe, дата выдачи первого удостоверения: 2010-05-20
- Владелец: Anna Johnson, дата выдачи первого удостоверения: 2012-12-05
- Владелец: Jane Doe, дата выдачи первого удостоверения: 2015-06-15
- Владелец: William Jenkins, дата выдачи первого удостоверения: 2015-09-25
- Владелец: Peter Brown, дата выдачи первого удостоверения: 2018-09-25
```