# Практическая работа 1

## Задание 1

Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов.

Был написана написана функция add_models(owners: int, cars: int) для добавления новых машин, владельцев и некоторых связей между ними

```python
def add_models(owners: int, cars: int):
    brands = ['brand1', 'brand2', 'brand3', 'brand4', 'brand5', 'brand6']
    models = ['model1', 'model2', 'model3', 'model4', 'model5', 'model6']
    colors = ['red', 'blue', 'brown', 'black', 'white', 'grey']
    fnames = ['oleg', 'sergey', 'dima', 'lyoha', 'vitek']
    lnames = ['l_name1', 'l_name2', 'l_name3', 'l_name4', 'l_name5', 'l_name6']

    id = int(Car.objects.last().id)
    owners = []
    cars = []
    for _ in range(n):
        id += 1
        brand = random.choice(brands)
        model = random.choice(models)
        color = random.choice(colors)
        number = random.randint(10**8, 10**9 - 1)
        car = Car.objects.create(gov_number=str(number), brand=brand, model=model, color=color)
        cars.append(car)
    id = int(CarOwner.objects.last().id)
    for _ in range(m):
        id += 1
        date = f'{random.randint(1990, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}'
        f_name = random.choice(fnames)
        l_name = random.choice(lnames)
        
        user = User.objects.create(name=f'{id}', passport_number=id, address='address', username=f'{id}')
        owner = CarOwner.objects.create(first_name=f_name, last_name=l_name, user=user)
        license = DriverLicence.objects.create(owner_id=owner, licence_number=f'{id}', type='ABC', date_of_issue=date)
        owners.append(owner)
    
    for owner in owners:
        ownership_count = random.randint(1, 3)
        for _ in range(ownership_count):
            car = random.choice(cars)
            date = f'{random.randint(2006, 2020)}-{random.randint(1, 12)}-{random.randint(1, 28)}'
            ownership = Ownership.objects.create(owner=owner, car=car, date_of_start=date)
```

## Задание 2

По созданным в пр.1 данным написать следующие запросы на фильтрацию:

* Где это необходимо, добавьте related_name к полям модели. Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
* Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
* Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
* Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
* Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

```python
from blog.models import Car, DriverLicence, CarOwner, Ownership, User

def get_cars_by_brand(brand: str):
    return Car.objects.filter(brand=brand)

def get_owners_by_fname(fname: str):
    return CarOwner.objects.filter(first_name=fname)

def get_driver_licence_by_owner(selected_owner: CarOwner):
    return DriverLicence.objects.get(owner_id=selected_owner.id)

def get_owners_by_car_color(color: str):
    return CarOwner.objects.filter(owner_car__car__color=color).distinct()

def get_owners_by_start_year(year: int | str):
    if type(year) == str:
        year = int(year)
    return CarOwner.objects.filter(owner_car__date_of_start__year__gte=year).distinct()

```

## Задание 3

Необходимо реализовать следующие запросы c применением описанных методов:

* Вывод даты выдачи самого старшего водительского удостоверения
* Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
* Выведите количество машин для каждого водителя
* Подсчитайте количество машин каждой марки
* Отсортируйте всех автовладельцев по дате выдачи удостоверения

```python
from blog.models import Car, DriverLicence, CarOwner, Ownership, User
from django.db.models import Min, Max, Count

def get_oldest_licence():
    return DriverLicence.objects.aggregate(date=Min("date_of_issue"))

def get_nearest_ownership():
    return Ownership.objects.exclude(date_of_finish=None).aggregate(date=Max('date_of_finish'))

def get_car_count_for_owners():
    a = CarOwner.objects.annotate(Count('car'))
    return {f'{o.first_name} {o.last_name}': o.car__count for o in a}

def count_cars_by_brand():
    return Car.objects.values('brand').annotate(Count('id'))

def sort_owners_by_licence_date():
    CarOwner.objects.order_by('owner_licence__date_of_issue')
```
