import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from project_first_app.models import CarOwner, DriverLicense, Car, Ownership


toyota_cars = Car.objects.filter(mark="Mark1")
for car in toyota_cars:
    print(f"Машина: {car.mark} {car.model}, номер: {car.state_number}")


user_owners = CarOwner.objects.filter(name="user2")
for owner in user_owners:
    print(f"Владелец: {owner.name} {owner.surname}, ID: {owner.id}")


random_owner = CarOwner.objects.all().last()
driver_license = DriverLicense.objects.get(owner_id=random_owner.id)
print(f"Номер удостоверения: {driver_license.license_number}, Владелец: {driver_license.owner_id.name}")


colour_cars = Car.objects.filter(colour="Colour1")
for car in colour_cars:
    owners = car.owners.all()
    for owner in owners:
        print(f"Владелец: {owner.name} {owner.surname}, Машина: {car.mark} {car.model}")


owners_2023 = Ownership.objects.filter(start_date__year__gte=2023)
for ownership in owners_2023:
    owner = ownership.owner_id
    print(f"Владелец: {owner.name} {owner.surname}, Машина: {ownership.car_id.mark} {ownership.car_id.model}")
