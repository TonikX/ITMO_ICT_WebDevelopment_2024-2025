import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jango_project_kuznetsov.settings")
django.setup()

from project_first_app.models import CarOwner, DriverLicense, Car, Ownership
from django.db.models import Count


oldest_license = DriverLicense.objects.earliest('date')
print(f"Самое старое удостоверение было выдано: {oldest_license.date}")


latest_ownership = Ownership.objects.latest('end_date')
print(f"Самая поздняя дата владения машиной: {latest_ownership.end_date}")


latest_ownership = Ownership.objects.latest('end_date')
print(f"Самая поздняя дата владения машиной: {latest_ownership.end_date}")


owners_with_car_count = CarOwner.objects.annotate(car_count=Count('cars'))
for owner in owners_with_car_count:
    print(f"Владелец {owner.name} {owner.surname} имеет {owner.car_count} машин")


car_count_by_mark = Car.objects.values('mark').annotate(car_count=Count('mark'))
for car in car_count_by_mark:
    print(f"Марка {car['mark']} встречается {car['car_count']} раз(а)")


owners_sorted_by_license_date = CarOwner.objects.filter(driver_licenses__isnull=False) \
    .distinct() \
    .order_by('driver_licenses__date')

for owner in owners_sorted_by_license_date:
    first_license = owner.driver_licenses.first()
    if first_license:
        print(f"Владелец {owner.name} {owner.surname}, дата выдачи удостоверения: {first_license.date}")
