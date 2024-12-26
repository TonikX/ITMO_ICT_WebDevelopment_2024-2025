import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jango_project_kuznetsov.settings")
django.setup()

from project_first_app.models import CarOwner, DriverLicense, Car, Ownership
from datetime import date

# -- Car Owners --

# CREATE
owners = [
    CarOwner(username=f"user{i}", surname=f"Surname{i}", name=f"Name{i}", birthday_date=date(1990+i, 1, 1))
    for i in range(2, 9)
]
CarOwner.objects.bulk_create(owners)

# GET
owners = CarOwner.objects.exclude(id=1)

# -- Cars --

# CREATE
cars = [
    Car(state_number=f"STATE-{i}", mark=f"Mark{i}", model=f"Model{i}", colour=f"Colour{i}")
    for i in range(1, 7)
]
Car.objects.bulk_create(cars)

# GET
cars = list(Car.objects.all())

# -- Driver License --
licenses = [
    DriverLicense(owner_id=owner, license_number=f"LIC-{i}", license_type="B", date=date(2020, 5, 1))
    for i, owner in enumerate(owners, start=1)
]
DriverLicense.objects.bulk_create(licenses)

# -- Ownerships
ownerships = []
for i, owner in enumerate(owners):
    assigned_cars = cars[i % len(cars):(i % len(cars)) + 2]
    for car in assigned_cars:
        ownerships.append(
            Ownership(owner_id=owner, car_id=car, start_date=date(2023, 1, 1), end_date=date(2024, 1, 1))
        )

Ownership.objects.bulk_create(ownerships)

# -- CHECK OBJECTS --
print("Автовладельцы:")
for owner in CarOwner.objects.exclude(id=1):
    print(f"{owner.name} {owner.surname}, ID: {owner.id}")

print("\nАвтомобили:")
for car in Car.objects.all():
    print(f"{car.mark} {car.model}, номер: {car.state_number}")

print("\nВодительские удостоверения:")
for license in DriverLicense.objects.all():
    print(f"Номер: {license.license_number}, Владелец: {license.owner_id.name}")

print("\nВладение автомобилями:")
for ownership in Ownership.objects.all():
    print(f"Владелец ID: {ownership.owner_id.id}, Автомобиль: {ownership.car_id.mark} {ownership.car_id.model}")
