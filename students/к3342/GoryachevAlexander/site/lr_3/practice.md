### Отчет по практическому заданию 

#### Условие
Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. 
Результатом должны стать запросы и отображение созданных объектов.

#### Выполнение 

Все запросы были сделаны в цикле в соответствующем  файле. 
Для начала нужно сгенерировать сущности, а уже потом записать их в таблицу с помощью нужного метода:
```python
<entity object>.objects.bulk_create(<array of entities>)
```

Например, автовладельцы генерируются следующим образом:
```python
owners = []
for i in range(2, 9):
    try:
        # проверка на существование пользователя
        existing_user = CarOwner.objects.filter(username=f"user{i}").first()
        if existing_user:
            owners.append(existing_user)
        else:
            owner = CarOwner(
                username=f"user{i}",
                surname=f"Surname{i}",
                name=f"Name{i}",
                birthday_date=date(1990+i, 1, 1)
            )
            owner.save()
            owners.append(owner)
    except IntegrityError as e:
        print(f"Could not create user{i}: {e}")
```
Аналогично формируем списки для машин:
```python
cars = [
    Car(state_number=f"STATE-{i}", mark=f"Mark{i}", model=f"Model{i}", colour=f"Colour{i}")
    for i in range(1, 7)
]
Car.objects.bulk_create(cars)
```
Лицензии машин:
```python
licenses = [
    DriverLicense(owner_id=owner, license_number=f"LIC-{i}", license_type="B", date=date(2020, 5, 1))
    for i, owner in enumerate(owners, start=1)
]
DriverLicense.objects.bulk_create(licenses)
```

И сущность владения машиной:
```python
ownerships = []
for i, owner in enumerate(owners):
    assigned_cars = cars[i % len(cars):(i % len(cars)) + 2]
    for car in assigned_cars:
        ownerships.append(
            Ownership(owner_id=owner, car_id=car, start_date=date(2023, 1, 1), end_date=date(2024, 1, 1))
        )

Ownership.objects.bulk_create(ownerships)
```

А следующим кодом можно все запринтить и убедиться в том, что все запросы применились 
```python
print("Автовладельцы:")
for owner in CarOwner.objects.exclude(id=1):
    print(f"{owner.name} {owner.surname}, ID: {owner.id}")
```

#### Условие

По созданным в пр.1 данным написать следующие запросы на фильтрацию:

0. Где это необходимо, добавьте related_name к полям модели
1. Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
2. Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
3. Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
4. Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
5. Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

#### Выполнение

Для всех моделей добавляем к каждому FK параметр `related_name` в shake_case.
После делаем запросы:

1. ```python
    toyota_cars = Car.objects.filter(mark="Mark1")
    for car in toyota_cars:
    print(f"Машина: {car.mark} {car.model}, номер: {car.state_number}")
   ```
2. ```python
    user_owners = CarOwner.objects.filter(name="user2")
    for owner in user_owners:
    print(f"Владелец: {owner.name} {owner.surname}, ID: {owner.id}")
   ```
3. ```python
    random_owner = CarOwner.objects.all().last()
    driver_license = DriverLicense.objects.get(owner_id=random_owner.id)
    print(f"Номер удостоверения: {driver_license.license_number}, Владелец: {driver_license.owner_id.name}")
   ```
4. ```python
    colour_cars = Car.objects.filter(colour="Colour1")
    for car in colour_cars:
        owners = car.owners.all()
        for owner in owners:
            print(f"Владелец: {owner.name} {owner.surname}, Машина: {car.mark} {car.model}")
   ```
5. ```python
    owners_2023 = Ownership.objects.filter(start_date__year__gte=2023)
    for ownership in owners_2023:
    owner = ownership.owner_id
    print(f"Владелец: {owner.name} {owner.surname}, Машина: {ownership.car_id.mark} {ownership.car_id.model}")
   ```



#### Условие

Необходимо реализовать следующие запросы c применением описанных методов:
1. Вывод даты выдачи самого старшего водительского удостоверения
2. Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
3. Выведите количество машин для каждого водителя
4. Подсчитайте количество машин каждой марки
5. Отсортируйте всех автовладельцев по дате выдачи удостоверения 

#### Выполнение
Запросы:

1. ```python
   oldest_license = DriverLicense.objects.earliest('date')
    print(f"Самое старое удостоверение было выдано: {oldest_license.date}")
   ```
2. ```python
    latest_ownership = Ownership.objects.latest('end_date')
    print(f"Самая поздняя дата владения машиной: {latest_ownership.end_date}")
   ```
3. ```python
    owners_with_car_count = CarOwner.objects.annotate(car_count=Count('cars'))
    for owner in owners_with_car_count:
        print(f"Владелец {owner.name} {owner.surname} имеет {owner.car_count} машин")
   ```
4. ```python
    car_count_by_mark = Car.objects.values('mark').annotate(car_count=Count('mark'))
    for car in car_count_by_mark:
        print(f"Марка {car['mark']} встречается {car['car_count']} раз(а)")
   ```
5. ```python
    owners_sorted_by_license_date = CarOwner.objects.filter(driver_licenses__isnull=False) \
    .distinct() \
    .order_by('driver_licenses__date')

    for owner in owners_sorted_by_license_date:
        first_license = owner.driver_licenses.first()
        if first_license:
            print(f"Владелец {owner.name} {owner.surname}, дата выдачи удостоверения: {first_license.date}")
   ```