import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_VEfimova.settings')
django.setup()


import datetime
from project_first_app.models import Car, CarOwner, Ownership, DrivingLicense

# Создаем автомобили
cars_data = [
    {"registration_number": "A111AA77", "brand": "Toyota", "model": "Camry", "color": "White"},
    {"registration_number": "B222BB77", "brand": "BMW", "model": "X5", "color": "Black"},
    {"registration_number": "C333CC77", "brand": "Mercedes", "model": "E-Class", "color": "Blue"},
    {"registration_number": "D444DD77", "brand": "Audi", "model": "A6", "color": "Gray"},
    {"registration_number": "E555EE77", "brand": "Hyundai", "model": "Tucson", "color": "Red"},
    {"registration_number": "F666FF77", "brand": "Kia", "model": "Rio", "color": "Green"},
]

cars = [Car(**car_data) for car_data in cars_data]
Car.objects.bulk_create(cars)

# Создаем владельцев
owners_data = [
    {"last_name": "Иванов", "first_name": "Иван", "birth_date": "1980-01-01"},
    {"last_name": "Петров", "first_name": "Петр", "birth_date": "1990-02-02"},
    {"last_name": "Сидоров", "first_name": "Сидор", "birth_date": "1975-03-03"},
    {"last_name": "Кузнецов", "first_name": "Алексей", "birth_date": "1985-04-04"},
    {"last_name": "Смирнов", "first_name": "Михаил", "birth_date": "1995-05-05"},
    {"last_name": "Попов", "first_name": "Андрей", "birth_date": "1988-06-06"},
]

owners = [CarOwner(**owner_data) for owner_data in owners_data]
CarOwner.objects.bulk_create(owners)

# Связываем владельцев с автомобилями через Ownership
cars = list(Car.objects.all())
owners = list(CarOwner.objects.all())

ownership_data = [
    {"owner": owners[0], "car": cars[0], "start_date": "2022-01-01", "end_date": None},
    {"owner": owners[0], "car": cars[1], "start_date": "2023-01-01", "end_date": None},
    {"owner": owners[1], "car": cars[2], "start_date": "2021-01-01", "end_date": None},
    {"owner": owners[2], "car": cars[3], "start_date": "2020-01-01", "end_date": None},
    {"owner": owners[3], "car": cars[4], "start_date": "2019-01-01", "end_date": None},
    {"owner": owners[4], "car": cars[5], "start_date": "2018-01-01", "end_date": None},
]

ownerships = [Ownership(**data) for data in ownership_data]
Ownership.objects.bulk_create(ownerships)

# Назначаем водительские удостоверения
licenses_data = [
    {"owner": owners[0], "license_number": "1234567890", "type": "B", "issue_date": "2010-01-01"},
    {"owner": owners[1], "license_number": "2233445566", "type": "C", "issue_date": "2015-01-01"},
    {"owner": owners[2], "license_number": "3344556677", "type": "D", "issue_date": "2020-01-01"},
    {"owner": owners[3], "license_number": "4455667788", "type": "A", "issue_date": "2005-01-01"},
    {"owner": owners[4], "license_number": "5566778899", "type": "B", "issue_date": "2000-01-01"},
]

licenses = [DrivingLicense(**data) for data in licenses_data]
DrivingLicense.objects.bulk_create(licenses)
