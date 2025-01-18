# Отчет на практическое задание 3.1

## Задание 1

### Описание

Добавить 6 новых автовладельцев и 5 автомобилей, назначив каждому владельцу от 1 до 3 машин.

```python
from project_first_app.models import CustomUser, Car, Ownership
from datetime import date

owner1 = CustomUser.objects.create_user(username="ivan_petrov", password="password123", passport_number="123987456")
owner2 = CustomUser.objects.create_user(username="olga_ivanova", password="password123", passport_number="456123789")
owner3 = CustomUser.objects.create_user(username="pavel_sidorov", password="password123", passport_number="789456123")
owner4 = CustomUser.objects.create_user(username="anna_kuznetsova", password="password123", passport_number="321654987")
owner5 = CustomUser.objects.create_user(username="sergey_volkov", password="password123", passport_number="654789321")
owner6 = CustomUser.objects.create_user(username="elena_rogozina", password="password123", passport_number="987321654")

car1 = Car.objects.create(make="Honda", model="Civic", color="Black", state_number="AAA123")
car2 = Car.objects.create(make="Hyundai", model="Elantra", color="Blue", state_number="BBB234")
car3 = Car.objects.create(make="Tesla", model="Model 3", color="White", state_number="CCC345")
car4 = Car.objects.create(make="Honda", model="Accord", color="Red", state_number="DDD456")
car5 = Car.objects.create(make="Hyundai", model="Santa Fe", color="Green", state_number="EEE567")

Ownership.objects.create(owner=owner1, car=car1, start_date=date(2024, 1, 1))
Ownership.objects.create(owner=owner1, car=car2, start_date=date(2024, 1, 15))
Ownership.objects.create(owner=owner2, car=car3, start_date=date(2024, 2, 1))
Ownership.objects.create(owner=owner3, car=car4, start_date=date(2024, 3, 1))
Ownership.objects.create(owner=owner4, car=car5, start_date=date(2024, 4, 1))
Ownership.objects.create(owner=owner5, car=car2, start_date=date(2024, 5, 1))
Ownership.objects.create(owner=owner6, car=car3, start_date=date(2024, 6, 1))
Ownership.objects.create(owner=owner6, car=car4, start_date=date(2024, 7, 1))
```

### Результат

- Владельцы
```python
ivan_petrov, olga_ivanova, pavel_sidorov, anna_kuznetsova, sergey_volkov, elena_rogozina
```

- Машины
```python
Honda Civic, Hyundai Elantra, Tesla Model 3, Honda Accord, Hyundai Santa Fe
```

## Задание 2

### Описание

Выполнить фильтрацию данных.

1. Все машины марки Honda:
```python
honda_cars = Car.objects.filter(make="Honda")
for car in honda_cars:
    print(car)
```

### Результат
```python
Honda Civic (AAA123)
Honda Accord (DDD456)
```

2. Владельцы, чьи имена начинаются на "Елена":
```python
elena_owners = CustomUser.objects.filter(username__icontains="elena")
for owner in elena_owners:
    print(owner)
```

### Результат
```python
elena_rogozina
```

3. Случайный автомобиль и его владелец:
```python
import random
random_car = random.choice(Car.objects.all())
owner = random_car.ownership_set.first().owner
print(f"Car: {random_car}, Owner: {owner.username}")
```

### Результат
```python
Car: Tesla Model 3, Owner: olga_ivanova
```

4. Все владельцы машин красного цвета:
```python
red_cars = Car.objects.filter(color="Red")
red_car_owners = CustomUser.objects.filter(ownerships__car__in=red_cars).distinct()
for owner in red_car_owners:
    print(owner)
```

### Результат
```python
pavel_sidorov
elena_rogozina
```

5. Владельцы машин с 2024 года:
```python
owners_from_2024 = CustomUser.objects.filter(ownerships__start_date__year=2024).distinct()
for owner in owners_from_2024:
    print(owner)
```

### Результат

```python
ivan_petrov
olga_ivanova
pavel_sidorov
anna_kuznetsova
sergey_volkov
elena_rogozina
```

## Задание 3

### Описание

Использовать аннотации и сортировки для анализа данных.

1. Самая ранняя дата начала владения машиной:

```python
earliest_ownership_date = Ownership.objects.earliest('start_date').start_date
print(f"The earliest ownership start date is: {earliest_ownership_date}")
```

### Результат
```python
The earliest ownership start date is: 2024-01-01
```

2. Количество машин у каждого владельца:
```python
owners_with_car_count = CustomUser.objects.annotate(car_count=Count('ownerships__car'))
for owner in owners_with_car_count:
    print(f"{owner.username} owns {owner.car_count} cars")
```

### Результат
```python
ivan_petrov owns 2 cars
olga_ivanova owns 1 cars
pavel_sidorov owns 1 cars
anna_kuznetsova owns 1 cars
sergey_volkov owns 1 cars
elena_rogozina owns 2 cars
```

3. Количество машин каждой марки:
```python
car_make_counts = Car.objects.values('make').annotate(count=Count('make'))
for make_count in car_make_counts:
    print(f"{make_count['make']}: {make_count['count']} cars")
```

### Результат
```python
Honda: 2 cars
Hyundai: 2 cars
Tesla: 1 cars
```

4. Сортировка владельцев по имени:
```python
sorted_users = CustomUser.objects.order_by('username')
for user in sorted_users:
    print(user.username)
```

### Результат
```python
anna_kuznetsova
elena_rogozina
ivan_petrov
olga_ivanova
pavel_sidorov
sergey_volkov
```