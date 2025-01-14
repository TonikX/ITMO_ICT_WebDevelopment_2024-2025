import os
import django
from django.utils import timezone
from datetime import datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab3.settings')
django.setup()

from lab3.models import CarOwner, Vehicle, DriveLicense, Ownership

def populate():
    owners_data = [
        {"surname": "Ivanov", "name": "Ivan", "birthDate": "1990-01-15"},
        {"surname": "Petrov", "name": "Petr", "birthDate": "1985-03-22"},
        {"surname": "Sidorov", "name": "Semyon", "birthDate": "1992-07-09"},
        {"surname": "Smirnov", "name": "Alexey", "birthDate": "1988-12-12"},
        {"surname": "Kuznetsov", "name": "Nikolay", "birthDate": "1995-06-05"},
        {"surname": "Popov", "name": "Andrey", "birthDate": "1993-08-21"},
        {"surname": "Volkov", "name": "Dmitry", "birthDate": "1991-11-10"},
    ]

    owners = []
    for data in owners_data:
        birth_date = timezone.make_aware(datetime.strptime(data["birthDate"], "%Y-%m-%d"))
        owner = CarOwner.objects.create(
            surname=data["surname"],
            name=data["name"],
            birthDate=birth_date
        )
        owners.append(owner)
        print(f"Создан автовладелец: {owner}")

    vehicles_data = [
        {"gosNumber": "A111AA", "brand": "Toyota", "model": "Camry", "color": "White"},
        {"gosNumber": "B222BB", "brand": "Honda", "model": "Civic", "color": "Black"},
        {"gosNumber": "C333CC", "brand": "Ford", "model": "Focus", "color": "Red"},
        {"gosNumber": "D444DD", "brand": "Nissan", "model": "Altima", "color": "Blue"},
        {"gosNumber": "E555EE", "brand": "Mazda", "model": "3", "color": "Gray"},
        {"gosNumber": "F666FF", "brand": "Hyundai", "model": "Elantra", "color": "Green"},
    ]

    vehicles = []
    for data in vehicles_data:
        vehicle = Vehicle.objects.create(
            gosNumber=data["gosNumber"],
            brand=data["brand"],
            model=data["model"],
            color=data["color"]
        )
        vehicles.append(vehicle)
        print(f"Создан автомобиль: {vehicle}")

    for owner in owners:
        license_number = f"LIC{random.randint(1000, 9999)}"
        license_type = random.choice(["A", "B", "C"])
        drive_license = DriveLicense.objects.create(
            id_owner=owner,
            license_number=license_number,
            type=license_type,
            data_issue=timezone.now()
        )
        print(f"Создано удостоверение для {owner}: {drive_license}")

        num_vehicles = random.randint(1, 3)
        assigned_vehicles = random.sample(vehicles, num_vehicles)
        for vehicle in assigned_vehicles:
            # Создаем запись о владении
            ownership = Ownership.objects.create(
                id_owner=owner,
                id_vehicle=vehicle,
                data_start=timezone.now()
            )
            print(f"{owner} теперь владеет автомобилем {vehicle}.")

if __name__ == "__main__":
    populate()