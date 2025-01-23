# Практическая работа №3.1: Django ORM - Запросы и их выполнение

## Описание

Эта работа направлена на освоение основных методов выполнения запросов в Django ORM, включая создание, фильтрацию, аннотирование и агрегацию данных. 
В рамках работы были созданы объекты для моделей, выполнены запросы для фильтрации данных, а также проведены аннотированные и агрегированные запросы для анализа данных.

## Цели работы

1. Ознакомиться с методами создания объектов через Django ORM.
2. Освоить выполнение базовых и сложных запросов с использованием Django ORM.
3. Научиться выполнять агрегированные и аннотированные запросы для анализа данных.
4. Закрепить знания по работе с полями Many-to-Many и связями между таблицами в Django.


### Задание 1: Создание объектов

1. Создать 6-7 автовладельцев (`CarOwner`), каждому из которых назначен пользователь (`User`).
2. Создать 5-6 автомобилей (`Car`) с различными характеристиками.
3. Назначить каждому владельцу удостоверение (`DrivingLicense`).
4. Присвоить каждому владельцу от 1 до 3 автомобилей через таблицу "владение" (`Ownership`).


```python
# Создание пользователей
user1 = User.objects.create_user(username="ivan", password="password123", passport_number="123456789", home_address="123 Main St", nationality="Russian")
# ...

# Создание владельцев автомобилей и связывание их с пользователями
owner1 = CarOwner.objects.create(user=user1, birth_date="1985-05-20")
# ...

# Создание автомобилей
car1 = Car.objects.create(registration_number="A123BC", make="Toyota", model="Camry", color="Red")
# ...

# Назначение водительских удостоверений для каждого владельца
license1 = DrivingLicense.objects.create(owner=owner1, license_number="L123456", license_type="B", issue_date=timezone.now())
# ...

# Создание записей владения автомобилями
Ownership.objects.create(car_owner=owner1, car=car1, start_date=timezone.make_aware(datetime(2022, 1, 1)), end_date=timezone.make_aware(datetime(2023, 1, 1)))
# ...
```


![telegram-cloud-photo-size-2-5289999764538124073-y.jpg](telegram-cloud-photo-size-2-5289999764538124073-y.jpg)
![telegram-cloud-photo-size-2-5289999764538124075-y.jpg](telegram-cloud-photo-size-2-5289999764538124075-y.jpg)
![telegram-cloud-photo-size-2-5289999764538124076-y.jpg](telegram-cloud-photo-size-2-5289999764538124076-y.jpg)
![telegram-cloud-photo-size-2-5289999764538124077-y.jpg](telegram-cloud-photo-size-2-5289999764538124077-y.jpg)
![telegram-cloud-photo-size-2-5289999764538124078-y.jpg](telegram-cloud-photo-size-2-5289999764538124078-y.jpg)


### Задание 2: Фильтрация данных

1. **Вывести все машины марки "Toyota".**
![telegram-cloud-photo-size-2-5296761988682214059-y.jpg](telegram-cloud-photo-size-2-5296761988682214059-y.jpg)   

2. **Найти всех водителей с именем "maria".**
![telegram-cloud-photo-size-2-5296761988682214062-y.jpg](telegram-cloud-photo-size-2-5296761988682214062-y.jpg)

3. **Получить экземпляр удостоверения по id случайного владельца (2 запроса).**
![telegram-cloud-photo-size-2-5296761988682214072-y.jpg](telegram-cloud-photo-size-2-5296761988682214072-y.jpg)

4. **Вывести всех владельцев красных машин.**
![telegram-cloud-photo-size-2-5296761988682214074-y.jpg](telegram-cloud-photo-size-2-5296761988682214074-y.jpg)

5. **Найти всех владельцев, чей год владения машиной начинается с 2021.**
![telegram-cloud-photo-size-2-5296761988682214079-y.jpg](telegram-cloud-photo-size-2-5296761988682214079-y.jpg)

### Задание 3: Агрегация и аннотация запросов

1. **Вывести дату выдачи самого старшего водительского удостоверения.**
![telegram-cloud-photo-size-2-5296761988682214081-y.jpg](telegram-cloud-photo-size-2-5296761988682214081-y.jpg)

2. **Самая поздняя дата владения машиной.**
![img_3.png](img_3.png)

3. **Количество машин для каждого водителя.**
![telegram-cloud-photo-size-2-5296761988682214084-y.jpg](telegram-cloud-photo-size-2-5296761988682214084-y.jpg)

4. **Количество машин каждой марки.**
![telegram-cloud-photo-size-2-5296761988682214092-y.jpg](telegram-cloud-photo-size-2-5296761988682214092-y.jpg)

5. **Сортировка автовладельцев по дате выдачи удостоверения.**
![telegram-cloud-photo-size-2-5296761988682214097-y.jpg](telegram-cloud-photo-size-2-5296761988682214097-y.jpg)

