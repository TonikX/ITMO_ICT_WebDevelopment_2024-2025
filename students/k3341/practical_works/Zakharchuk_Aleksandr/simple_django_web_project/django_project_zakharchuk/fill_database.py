import secrets

from project_first_app import models


# create owners
owner1 = models.Owner(first_name="Ivan", last_name="Ivanov", username="ivan_ivanov")
owner1.save()

owner2 = models.Owner(first_name="Petr", last_name="Petrov", username="petr_petrov")
owner2.save()

owner3 = models.Owner(first_name="John", last_name="Doe", username="john_doe")
owner3.save()

owner4 = models.Owner(first_name="Rick", last_name="Sanchez", username="rick_sanchez")
owner4.save()

owner5 = models.Owner(first_name="Peter", last_name="Griffin", username="peter_griffin")
owner5.save()

owner6 = models.Owner(first_name="Homer", last_name="Simpson", username="homer_simpson")
owner6.save()

# create licenses
licenses = [
    models.DriverLicense(owner_id=owner1, license_number=secrets.token_hex(10), type="B"),
    models.DriverLicense(owner_id=owner2, license_number=secrets.token_hex(10), type="B"),
    models.DriverLicense(owner_id=owner3, license_number=secrets.token_hex(10), type="B"),
    models.DriverLicense(owner_id=owner4, license_number=secrets.token_hex(10), type="B"),
    models.DriverLicense(owner_id=owner5, license_number=secrets.token_hex(10), type="B"),
    models.DriverLicense(owner_id=owner6, license_number=secrets.token_hex(10), type="B"),
]

models.DriverLicense.objects.bulk_create(licenses)
print(models.DriverLicense.objects.all())

# create cars
cars = [
    models.Car(number=secrets.token_hex(6), brand="Tesla", model="Model Y", color="blue"),
    models.Car(number=secrets.token_hex(6), brand="Lucid", model="Saphire", color="black"),
    models.Car(number=secrets.token_hex(6), brand="Haval", model="F6", color="white"),
    models.Car(number=secrets.token_hex(6), brand="Toyota", model="Camry", color="gray"),
    models.Car(number=secrets.token_hex(6), brand="Nissan", model="Almera", color="gray"),
    models.Car(number=secrets.token_hex(6), brand="Audi", model="TT", color="black"),
]

models.Car.objects.bulk_create(cars)
print(models.Car.objects.all())

# create ownerships
ownerships = [
    models.Ownership(owner_id=owner1, car_id=cars[0]),
    models.Ownership(owner_id=owner2, car_id=cars[1]),
    models.Ownership(owner_id=owner3, car_id=cars[2]),
    models.Ownership(owner_id=owner4, car_id=cars[3]),
    models.Ownership(owner_id=owner5, car_id=cars[4]),
    models.Ownership(owner_id=owner6, car_id=cars[5]),
]

models.Ownership.objects.bulk_create(ownerships)
print(models.Ownership.objects.all())
