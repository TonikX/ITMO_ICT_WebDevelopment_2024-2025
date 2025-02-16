from project_first_app.models import AutoOwner, Auto, Ownership, DriverLicense
import random

toyota_cars = Auto.objects.filter(brand="Toyota")
for car in toyota_cars:
    print(car)

drivers_named = AutoOwner.objects.filter(name="Petr")
for driver in drivers_named:
    print(driver)

random_owner = AutoOwner.objects.order_by('?').first()
owner_id = random_owner.id_owner

driver_license = DriverLicense.objects.get(id_owner=random_owner)
print(f"Владелец: {random_owner}, Удостоверение: {driver_license}")

owners_black_cars = AutoOwner.objects.filter(autos__color="Black").distinct()
for owner in owners_black_cars:
    print(owner)

owners_2025 = AutoOwner.objects.filter(ownership__start_date__year=2025).distinct()
for owner in owners_2025:
    print(owner)