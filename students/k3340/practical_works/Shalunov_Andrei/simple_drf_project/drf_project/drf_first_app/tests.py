from datetime import date
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
    DriverLicense.objects.create(
        owner=owner,
        license_number=f"UD{i+1:05}",
        category="B",
        date_of_issue=date(2020, 1, 1)
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