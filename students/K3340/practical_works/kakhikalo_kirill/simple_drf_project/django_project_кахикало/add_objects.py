import random
from datetime import date, timedelta, datetime
from project_first_app.models import AutoOwner, Auto, Ownership, DriverLicense

owners_data = [
    {"surname": "Ivanov", "name": "Ivan", "date_of_birth": "1985-06-15", "username": "ivanov"},
    {"surname": "Petrov", "name": "Petr", "date_of_birth": "1990-03-22", "username": "petrov"},
    {"surname": "Sidorov", "name": "Sergey", "date_of_birth": "1988-11-10", "username": "sidorov"},
    {"surname": "Smirnov", "name": "Alexey", "date_of_birth": "1995-09-05", "username": "smirnov"},
    {"surname": "Fedorov", "name": "Fedor", "date_of_birth": "1982-12-30", "username": "fedorov"},
    {"surname": "Kuznetsov", "name": "Dmitry", "date_of_birth": "1993-07-18", "username": "kuznetsov"},
]

cars_data = [
    {"state_number": "A123BC", "brand": "Toyota", "model": "Camry", "color": "Black"},
    {"state_number": "B456DE", "brand": "Honda", "model": "Civic", "color": "White"},
    {"state_number": "C789FG", "brand": "BMW", "model": "X5", "color": "Blue"},
    {"state_number": "D101HI", "brand": "Mercedes", "model": "E-Class", "color": "Silver"},
    {"state_number": "E202JK", "brand": "Ford", "model": "Focus", "color": "Red"},
    {"state_number": "F303LM", "brand": "Nissan", "model": "Qashqai", "color": "Green"},
    {"state_number": "G404NO", "brand": "Audi", "model": "A4", "color": "Gray"},
    {"state_number": "H505PQ", "brand": "Chevrolet", "model": "Malibu", "color": "Blue"},
    {"state_number": "I606RS", "brand": "Volkswagen", "model": "Passat", "color": "White"},
    {"state_number": "J707TU", "brand": "Kia", "model": "Sorento", "color": "Black"},
    {"state_number": "K808VW", "brand": "Hyundai", "model": "Sonata", "color": "Silver"},
    {"state_number": "L909XY", "brand": "Subaru", "model": "Forester", "color": "Green"},
]

owners = []
for owner in owners_data:
    new_owner = AutoOwner.objects.create(
        surname=owner["surname"],
        name=owner["name"],
        date_of_birth=owner["date_of_birth"],
        username=owner["username"]
    )
    owners.append(new_owner)

cars = []
for car in cars_data:
    new_car = Auto.objects.create(
        state_number=car["state_number"],
        brand=car["brand"],
        model=car["model"],
        color=car["color"]
    )
    cars.append(new_car)

def random_date(start_year=2000, end_year=date.today().year):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta_days = (end - start).days
    random_days = random.randint(0, delta_days)
    return start + timedelta(days=random_days)

for owner in owners:
    DriverLicense.objects.create(
        id_owner=owner,
        license_number=f"{random.randint(100000, 999999)}",
        type=random.choice(["B", "C", "D"]),
        date_of_issue=random_date(2000, date.today().year)
    )

if len(cars) < len(owners):
    raise ValueError("Not enough cars to ensure every owner has one.")

remaining_cars = cars.copy()
random.shuffle(remaining_cars)

for owner in owners:
    car = remaining_cars.pop()
    Ownership.objects.create(
        id_owner=owner,
        id_auto=car,
        start_date=random_date(2000, date.today().year)
    )

while remaining_cars:
    car = remaining_cars.pop()
    owner = random.choice(owners)
    Ownership.objects.create(
        id_owner=owner,
        id_auto=car,
        start_date=random_date(2000, date.today().year)
    )

for owner in owners:
    owned_cars = Ownership.objects.filter(id_owner=owner)
    car_brands = [ownership.id_auto.brand for ownership in owned_cars]
    print(f"Owner: {owner.surname} {owner.name}, Cars: {car_brands}")
