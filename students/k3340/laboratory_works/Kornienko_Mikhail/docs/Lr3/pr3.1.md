
# Отчет на практическое задание 3.1

## Задание 1

### Описание

Добавить 6 новых автовладельцев и 5 автомобилей, назначив каждому владельцу от 1 до 3 машин.

```python
from project_first_app.models import CustomUser, Car, Ownership
from datetime import date

# Создаем владельцев
owner1 = CustomUser.objects.create_user(username="andrey_pavlov", password="pass123", passport_number="123456789")
owner2 = CustomUser.objects.create_user(username="maria_smirnova", password="pass123", passport_number="987654321")
owner3 = CustomUser.objects.create_user(username="sergey_kuzmin", password="pass123", passport_number="456789123")
owner4 = CustomUser.objects.create_user(username="olga_orlova", password="pass123", passport_number="321987654")
owner5 = CustomUser.objects.create_user(username="dmitry_ivanov", password="pass123", passport_number="654123987")
owner6 = CustomUser.objects.create_user(username="tatiana_volkova", password="pass123", passport_number="789123456")

# Создаем автомобили
car1 = Car.objects.create(make="BMW", model="3 Series", color="White", state_number="XYZ111")
car2 = Car.objects.create(make="Audi", model="A4", color="Blue", state_number="XYZ222")
car3 = Car.objects.create(make="Mercedes", model="C-Class", color="Black", state_number="XYZ333")
car4 = Car.objects.create(make="BMW", model="5 Series", color="Red", state_number="XYZ444")
car5 = Car.objects.create(make="Audi", model="Q5", color="Green", state_number="XYZ555")

# Назначаем автомобили владельцам
Ownership.objects.create(owner=owner1, car=car1, start_date=date(2024, 1, 10))
Ownership.objects.create(owner=owner1, car=car2, start_date=date(2024, 1, 20))
Ownership.objects.create(owner=owner2, car=car3, start_date=date(2024, 2, 15))
Ownership.objects.create(owner=owner3, car=car4, start_date=date(2024, 3, 5))
Ownership.objects.create(owner=owner4, car=car5, start_date=date(2024, 4, 1))
Ownership.objects.create(owner=owner5, car=car2, start_date=date(2024, 5, 10))
Ownership.objects.create(owner=owner6, car=car3, start_date=date(2024, 6, 12))
Ownership.objects.create(owner=owner6, car=car4, start_date=date(2024, 7, 20))
```

### Результат

- Владельцы:
```python
andrey_pavlov, maria_smirnova, sergey_kuzmin, olga_orlova, dmitry_ivanov, tatiana_volkova
```

- Машины:
```python
BMW 3 Series, Audi A4, Mercedes C-Class, BMW 5 Series, Audi Q5
```

## Задание 2

### Описание

Выполнить фильтрацию данных.

1. Все машины марки BMW:
```python
bmw_cars = Car.objects.filter(make="BMW")
for car in bmw_cars:
    print(car)
```

### Результат
```python
BMW 3 Series (XYZ111)
BMW 5 Series (XYZ444)
```

2. Владельцы, чьи имена содержат "tatiana":
```python
tatiana_owners = CustomUser.objects.filter(username__icontains="tatiana")
for owner in tatiana_owners:
    print(owner)
```

### Результат
```python
tatiana_volkova
```

3. Случайный автомобиль и его владелец:
```python
import random
random_car = random.choice(list(Car.objects.all()))
owner = random_car.ownership_set.first().owner
print(f"Car: {random_car}, Owner: {owner.username}")
```

### Результат
```python
Car: Audi A4, Owner: andrey_pavlov
```

4. Все владельцы машин черного цвета:
```python
black_cars = Car.objects.filter(color="Black")
black_car_owners = CustomUser.objects.filter(ownerships__car__in=black_cars).distinct()
for owner in black_car_owners:
    print(owner)
```

### Результат
```python
maria_smirnova
tatiana_volkova
```

5. Владельцы машин, начавшие владение с 2024 года:
```python
owners_from_2024 = CustomUser.objects.filter(ownerships__start_date__year=2024).distinct()
for owner in owners_from_2024:
    print(owner)
```

### Результат
```python
andrey_pavlov
maria_smirnova
sergey_kuzmin
olga_orlova
dmitry_ivanov
tatiana_volkova
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
The earliest ownership start date is: 2024-01-10
```

2. Количество машин у каждого владельца:
```python
from django.db.models import Count

owners_with_car_count = CustomUser.objects.annotate(car_count=Count('ownerships__car'))
for owner in owners_with_car_count:
    print(f"{owner.username} owns {owner.car_count} cars")
```

### Результат
```python
andrey_pavlov owns 2 cars
maria_smirnova owns 1 car
sergey_kuzmin owns 1 car
olga_orlova owns 1 car
dmitry_ivanov owns 1 car
tatiana_volkova owns 2 cars
```

3. Количество машин каждой марки:
```python
car_make_counts = Car.objects.values('make').annotate(count=Count('make'))
for make_count in car_make_counts:
    print(f"{make_count['make']}: {make_count['count']} cars")
```

### Результат
```python
BMW: 2 cars
Audi: 2 cars
Mercedes: 1 car
```

4. Сортировка владельцев по имени:
```python
sorted_users = CustomUser.objects.order_by('username')
for user in sorted_users:
    print(user.username)
```

### Результат
```python
andrey_pavlov
dmitry_ivanov
maria_smirnova
olga_orlova
sergey_kuzmin
tatiana_volkova
```
