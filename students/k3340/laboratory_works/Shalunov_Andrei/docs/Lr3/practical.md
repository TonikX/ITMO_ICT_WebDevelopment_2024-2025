# Отчет по Практической Работе №3.1

## **Практическое задание 1:**

### **Описание**
Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов. 

```html
from datetime import date, timedelta
from drf_first_app.models import Owner, DriverLicense, Car, Ownership

owners = [
    Owner.objects.get_or_create(username="ivanov", defaults={"first_name": "Иван", "last_name": "Иванов", "birthday_date": "1990-01-01"})[0],
    Owner.objects.get_or_create(username="petrov", defaults={"first_name": "Петр", "last_name": "Петров", "birthday_date": "1985-05-15"})[0],
    Owner.objects.get_or_create(username="sidorov", defaults={"first_name": "Сергей", "last_name": "Сидоров", "birthday_date": "1978-11-20"})[0],
    Owner.objects.get_or_create(username="kuznetsov", defaults={"first_name": "Алексей", "last_name": "Кузнецов", "birthday_date": "1995-07-10"})[0],
    Owner.objects.get_or_create(username="morozov", defaults={"first_name": "Дмитрий", "last_name": "Морозов", "birthday_date": "1980-03-30"})[0],
    Owner.objects.get_or_create(username="vasiliev", defaults={"first_name": "Андрей", "last_name": "Васильев", "birthday_date": "1992-09-25"})[0],
]

cars = [
    Car.objects.get_or_create(state_number="A123BC", defaults={"brand": "Toyota", "model": "Camry", "color": "Белый"})[0],
    Car.objects.get_or_create(state_number="B456CD", defaults={"brand": "BMW", "model": "X5", "color": "Черный"})[0],
    Car.objects.get_or_create(state_number="C789DE", defaults={"brand": "Audi", "model": "Q7", "color": "Синий"})[0],
    Car.objects.get_or_create(state_number="D321FG", defaults={"brand": "Mercedes", "model": "GLC", "color": "Серебристый"})[0],
    Car.objects.get_or_create(state_number="E654HI", defaults={"brand": "Honda", "model": "Civic", "color": "Красный"})[0],
    Car.objects.get_or_create(state_number="F987JK", defaults={"brand": "Ford", "model": "Focus", "color": "Зеленый"})[0],
]

for i, owner in enumerate(owners):
    DriverLicense.objects.get_or_create(
        owner=owner,
        defaults={
            "license_number": f"UD{i+1:05}",
            "category": "B",
            "date_of_issue": date(2024, 1, 1) + timedelta(days=i),
        }
    )

ownerships = [
    Ownership.objects.create(owner=owners[0], car=cars[0], start_date=date(2022, 1, 1)),
    Ownership.objects.create(owner=owners[0], car=cars[1], start_date=date(2022, 1, 1)),
    Ownership.objects.create(owner=owners[1], car=cars[2], start_date=date(2022, 2, 1)),
    Ownership.objects.create(owner=owners[2], car=cars[3], start_date=date(2022, 3, 1)),
    Ownership.objects.create(owner=owners[3], car=cars[4], start_date=date(2022, 4, 1)),
    Ownership.objects.create(owner=owners[4], car=cars[5], start_date=date(2022, 5, 1)),
    Ownership.objects.create(owner=owners[5], car=cars[0], start_date=date(2022, 6, 1)),
]

print("Владельцы:")
for owner in Owner.objects.all():
    print(owner)

print("\nАвтомобили:")
for car in Car.objects.all():
    print(car)

print("\nВодительские удостоверения:")
for license in DriverLicense.objects.all():
    print(license)

print("\nВладения:")
for ownership in Ownership.objects.all():
    print(ownership)
```
#### Владельцы:
```
Иван Иванов
Петр Петров
Сергей Сидоров
Алексей Кузнецов
Дмитрий Морозов
Андрей Васильев
```

#### Автомобили:
```
Toyota Camry A123BC
BMW X5 B456CD
Audi Q7 C789DE
Mercedes GLC D321FG
Honda Civic E654HI
Ford Focus F987JK
```

#### Водительские удостоверения:
```
License UD00001 for Иван Иванов
License UD00002 for Петр Петров
License UD00003 for Сергей Сидоров
License UD00004 for Алексей Кузнецов
License UD00005 for Дмитрий Морозов
License UD00006 for Андрей Васильев
```

#### Владения:
```
Иван Иванов owns Toyota Camry A123BC from 2022-01-01 to present
Иван Иванов owns BMW X5 B456CD from 2022-01-01 to present
Петр Петров owns Audi Q7 C789DE from 2022-02-01 to present
Сергей Сидоров owns Mercedes GLC D321FG from 2022-03-01 to present
Алексей Кузнецов owns Honda Civic E654HI from 2022-04-01 to present
Дмитрий Морозов owns Ford Focus F987JK from 2022-05-01 to present
Андрей Васильев owns Toyota Camry A123BC from 2022-06-01 to present
```

## **Практическое задание 2:**
### Выведете все машины марки “Toyota”
```
toyota_cars = Car.objects.filter(brand="Toyota")
for car in toyota_cars:
    print(car)
```
#### Результат
```
Toyota Camry A123BC
```

### Найти всех водителей с именем “Андрей”
```python
andrew_drivers =  Owner.objects.filter(first_name__contains="Андрей")
for driver in andrew_drivers:
    print(driver)
```
#### Результат
```
Андрей Васильев
```

### Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
```python
import random
random_driver = random.choice(Owner.objects.all())
driver_license = DriverLicense.objects.get(owner__id=random_driver.id)
print(f"Удостоверение: {driver_license}")
```

#### Результат
```
Удостоверение: License UD00002 for Петр Петров
```
### Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
```python
red_car_owners = Owner.objects.filter(ownerships__car__color="Красный").distinct()
for owner in red_car_owners:
    print(owner)
```

#### Результат
```
Алексей Кузнецов
```
### Найти всех владельцев, чей год владения машиной начинается с 2022 (или любой другой год, который присутствует у вас в базе)
```python
new_cars = Owner.objects.filter(ownerships__start_date__year=2022).distinct()
for owner in new_cars:
    print(owner)
```
#### Результат
```
Иван Иванов
Алексей Кузнецов
Дмитрий Морозов
Петр Петров
Сергей Сидоров
Андрей Васильев
```

## **Практическое задание 3:**
### Вывод даты выдачи самого старшего водительского удостоверения
```python
from django.db.models import Min

oldest_license_date = DriverLicense.objects.aggregate(Min("date_of_issue"))["date_of_issue__min"]
print(f"Самая ранняя дата выдачи удостоверения: {oldest_license_date}")
```
#### Результат
```
Самая ранняя дата выдачи удостоверения: 2024-01-01
```

### Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
```python
from django.db.models import Max

latest_ownership_date = Ownership.objects.aggregate(Max('end_date'))['end_date__max']
print(f"Самая поздняя дата владения машиной: {latest_ownership_date}")
```
#### Результат
```
Самая поздняя дата владения машиной: 2023-06-01
```

### Выведите количество машин для каждого водителя
```python
from django.db.models import Count

counter_cars = Owner.objects.annotate(car_count = Count("ownerships__car"))
for owner in counter_cars:
    print(f"{owner.first_name} {owner.last_name}: {owner.car_count} машин(ы)")
```
#### Результат
```
Иван Иванов: 2 машин(ы)
Алексей Кузнецов: 1 машин(ы)
Дмитрий Морозов: 1 машин(ы)
Петр Петров: 1 машин(ы)
Сергей Сидоров: 1 машин(ы)
Андрей Васильев: 1 машин(ы)
```

### Подсчитайте количество машин каждой марки
```python
counts_by_brand = Car.objects.values("brand").annotate(car_count=Count("id"))
for brand in counts_by_brand:
    print(f"Марка {brand['brand']}: {brand['car_count']} машин(ы)")
```
#### Результат
```
Марка Audi: 1 машин(ы)
Марка BMW: 2 машин(ы)
Марка Ford: 1 машин(ы)
Марка Honda: 1 машин(ы)
Марка Mercedes: 1 машин(ы)
Марка Toyota: 1 машин(ы)
```

### Отсортируйте всех автовладельцев по дате выдачи удостоверения
```python
sorted_owners = Owner.objects.filter(licenses__isnull=False).distinct().order_by('licenses__date_of_issue')
for owner in sorted_owners:
    first_license_date = owner.licenses.order_by("date_of_issue").first().date_of_issue
    print(f"{owner.first_name} {owner.last_name} {first_license_date}")
```

#### Результат
```
Иван Иванов 2024-01-01
Петр Петров 2024-01-02
Сергей Сидоров 2024-01-03
Алексей Кузнецов 2024-01-04
Дмитрий Морозов 2024-01-05
Андрей Васильев 2024-01-06
```