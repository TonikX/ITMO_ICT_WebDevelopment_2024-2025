# Практическая работа 1

## Задание 1. Создание объектов
Необходимо создать несколько объектов и поместить их в БД:
```python
from datetime import date, timedelta
from project_second_app.models import Car, CarOwner, DrivingLicence, Ownership

car1 = Car.objects.create(car_number="A123BC77", brand="Toyota", model="Corolla", color="Red")
car2 = Car.objects.create(car_number="B456CD77", brand="Honda", model="Civic", color="Blue")
car3 = Car.objects.create(car_number="C789DE77", brand="Ford", model="Focus", color="Black")
car4 = Car.objects.create(car_number="D101EF77", brand="BMW", model="X5", color="White")
car5 = Car.objects.create(car_number="E202GH77", brand="Audi", model="A4", color="Silver")
car6 = Car.objects.create(car_number="F303IJ77", brand="Nissan", model="Altima", color="Green")

owner1 = CarOwner.objects.create(first_name="John", last_name="Doe", passport_number="1234567890", nationality="USA")
owner2 = CarOwner.objects.create(first_name="Jane", last_name="Doe", passport_number="0987654321", nationality="Canada")
owner3 = CarOwner.objects.create(first_name="Alex", last_name="Smith", passport_number="5678901234", nationality="UK")
owner4 = CarOwner.objects.create(first_name="Emily", last_name="Johnson", passport_number="4321098765", nationality="Australia")
owner5 = CarOwner.objects.create(first_name="Michael", last_name="Brown", passport_number="2468135790", nationality="Germany")
owner6 = CarOwner.objects.create(first_name="Sarah", last_name="Williams", passport_number="1357913579", nationality="France")
owner7 = CarOwner.objects.create(first_name="Oleg", last_name="Ivanov", passport_number="9876543210", nationality="Russia")

DrivingLicence.objects.create(car_owner=owner1, license_number="DL12345", license_type="B", issue_date=date(2020, 5, 15))
DrivingLicence.objects.create(car_owner=owner2, license_number="DL23456", license_type="B", issue_date=date(2021, 7, 10))
DrivingLicence.objects.create(car_owner=owner3, license_number="DL34567", license_type="A", issue_date=date(2019, 8, 20))
DrivingLicence.objects.create(car_owner=owner4, license_number="DL45678", license_type="B", issue_date=date(2022, 2, 25))
DrivingLicence.objects.create(car_owner=owner5, license_number="DL56789", license_type="A", issue_date=date(2020, 11, 5))
DrivingLicence.objects.create(car_owner=owner6, license_number="DL67890", license_type="B", issue_date=date(2021, 1, 30))
DrivingLicence.objects.create(car_owner=owner7, license_number="DL78901", license_type="B", issue_date=date(2022, 4, 10))


def add_ownership(car, owner, start_date, duration_days=365):
    end_date = start_date + timedelta(days=duration_days)
    Ownership.objects.create(car_owner=owner, car=car, start_date=start_date, end_date=end_date)

add_ownership(car1, owner1, date(2020, 1, 1))
add_ownership(car2, owner2, date(2021, 1, 1))
add_ownership(car3, owner3, date(2022, 1, 1))
add_ownership(car4, owner4, date(2021, 6, 1), duration_days=200)
add_ownership(car5, owner5, date(2020, 5, 1))
add_ownership(car6, owner6, date(2023, 1, 1), duration_days=500)
```

## Задание 2. Создание простых запросов 
По созданным в пр.1 данным написать следующие запросы на фильтрацию:
* Где это необходимо, добавьте related_name к полям модели
* Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
* Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
* Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
* Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
* Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

Сначала добавим `related_name` в наши модели. 
```python
class CarOwner(models.Model):
    ...
    cars = models.ManyToManyField(Car, through="Ownership", related_name="owners")
    ...


class Ownership(models.Model):
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name="ownerships")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ownerships")
    ...
```

И не забудем про миграции:
```shell
python manage.py makemigrations
python manage.py migrate
```

Теперь можно приступать к заданиям. 

---
Выведете все машины марки “Toyota”
```python
>>> Car.objects.filter(brand="Toyota")
# <QuerySet [<Car: Toyota Corolla (A123BC77)>]>
```

Найти всех водителей с именем “Олег”
```python
>>> CarOwner.objects.filter(first_name="Oleg")
# <QuerySet [<CarOwner: Oleg Ivanov>]>
```

Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели
```python
>>> DrivingLicence.objects.get(car_owner=CarOwner.objects.first())
# <DrivingLicence: DrivingLicence object (15)>
```

Вывести всех владельцев красных машин
```python
>>> CarOwner.objects.filter(cars__color="Red").distinct()
# <QuerySet [<CarOwner: John Doe>]>
```

Найти всех владельцев, чей год владения машиной начинается с 2022
```python
>>> CarOwner.objects.filter(ownerships__start_date__year__gte=2022).distinct()
# <QuerySet [<CarOwner: Alex Smith>, <CarOwner: Sarah Williams>]>
```

## Задание 3. Агрегация и аннотация запросов

Начнём с импорта всех необходимых частей
```python
from django.db.models import Min, Max, Count
```


Вывод даты выдачи самого старшего водительского удостоверения
```python
DrivingLicence.objects.aggregate(Min('issue_date'))['issue_date__min']
```

Самая поздняя дата владения машиной
> Учитываем только записи, где end_date не равно None.
```python
Ownership.objects.exclude(end_date__isnull=True).aggregate(Max('end_date'))['end_date__max']
```

Для следующих заданий добавим функцию для правильного склонения слов
```python
def num_word(value, words):
    num = value % 100
    if num > 19:
        num = num % 10

    if num == 1:
        return words[0]
    elif 2 <= num <= 4:
        return words[1]
    else:
        return words[2]
```

Выведите количество машин для каждого водителя
```python
for owner in CarOwner.objects.annotate(car_count=Count('cars')).order_by('-car_count'):
    word = num_word(owner.car_count, ["машину", "машины", "машин"])
    print(f"{owner.first_name} {owner.last_name} имеет {owner.car_count} {word}.")
```

Подсчитайте количество машин каждой марки
```python
cars_per_brand = Car.objects.values('brand').annotate(car_count=Count('id')).order_by('-car_count')
for entry in cars_per_brand:
    word = num_word(entry['car_count'], ["раз", "раза", "раз"])
    print(f"Марка {entry['brand']} встречается {entry['car_count']} {word}.")
```

Отсортируйте всех автовладельцев по дате выдачи удостоверения
```python
owners_sorted_by_license_date = CarOwner.objects.filter(drivinglicence__isnull=False).distinct().order_by('drivinglicence__issue_date')
for owner in owners_sorted_by_license_date:
    license_date = owner.drivinglicence_set.first().issue_date
    print(f"{owner.first_name} {owner.last_name}: дата выдачи удостоверения - {license_date}")
```
