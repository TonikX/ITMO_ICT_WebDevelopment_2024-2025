#1. Вывести все машины марки “Toyota”
from lab3.models import Vehicle

toyota_cars = Vehicle.objects.filter(brand="Toyota")
for car in toyota_cars:
    print(car)
#2. Найти всех водителей с именем “Олег”
from lab3.models import CarOwner

oleg_drivers = CarOwner.objects.filter(name="Alexey")
for driver in oleg_drivers:
    print(driver)

#3.Получить удостоверение по ID случайного владельца
from lab3.models import CarOwner, DriveLicense
import random

owners = CarOwner.objects.all()
random_owner = random.choice(owners)

owner_id = random_owner.id_owner
print(f"Owner ID: {owner_id}")

license = DriveLicense.objects.get(id_owner=owner_id)
print(license)

#4. Вывести всех владельцев красных машин
from lab3.models import Vehicle, Ownership, CarOwner

red_cars = Vehicle.objects.filter(color="Red")


for car in red_cars:
    owners = car.ownerships.all()
    for ownership in owners:
        print(ownership.id_owner)
#5. Найти всех владельцев, чей год владения машиной начинается с 2010 года
from lab3.models import Ownership

owners_2010 = Ownership.objects.filter(data_start__year=2010)
for ownership in owners_2010:
    print(ownership.id_owner)

#1. Вывод даты выдачи самого старшего водительского удостоверения
from lab3.models import DriveLicense

oldest_license = DriveLicense.objects.earliest('data_issue')
print(f"Дата выдачи самого старого удостоверения: {oldest_license.data_issue}")
#2. Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей
from lab3.models import Vehicle, Ownership

# Получаем самую позднюю дату владения для машин, которые есть в базе
latest_ownership = Ownership.objects.filter(id_vehicle__in=Vehicle.objects.all()).latest('data_start')
print(f"Самая поздняя дата владения машиной: {latest_ownership.data_start}")
#3. Выведите количество машин для каждого водителя
from django.db.models import Count
from lab3.models import CarOwner

owners_car_count = CarOwner.objects.annotate(num_cars=Count('ownerships')).values('surname', 'name', 'num_cars')

for owner in owners_car_count:
    print(f"{owner['surname']} {owner['name']} - {owner['num_cars']} машин")
#4. Подсчитайте количество машин каждой марки:
from django.db.models import Count
from lab3.models import Vehicle

car_counts_by_brand = Vehicle.objects.values('brand').annotate(num_cars=Count('brand'))

for car in car_counts_by_brand:
    print(f"{car['brand']} - {car['num_cars']}")
#5. Отсортируйте всех автовладельцев по дате выдачи удостоверения (с использованием .distinct())
from lab3.models import CarOwner

owners_sorted_by_license_date = CarOwner.objects.filter(licenses__isnull=False).distinct().order_by('licenses__data_issue')

for owner in owners_sorted_by_license_date:
    print(f"{owner.name} - {owner.licenses.first().data_issue}")