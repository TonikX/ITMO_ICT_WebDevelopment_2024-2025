from project_first_app.models import AutoOwner, Auto, Ownership, DriverLicense
from django.db.models import Count, Min, Max


oldest_license = DriverLicense.objects.aggregate(earliest_date=Min('date_of_issue'))
print("Дата выдачи самого старого водительского удостоверения:",
      oldest_license['earliest_date'])

latest_ownership = Ownership.objects.aggregate(latest_date=Max('start_date'))
print("Самая поздняя дата владения машиной:",
      latest_ownership['latest_date'])

owners_with_car_count = AutoOwner.objects.annotate(car_count=Count('ownership'))
print("Количество машин для каждого водителя:")
for owner in owners_with_car_count:
    print(f"{owner.surname} {owner.name}: {owner.car_count} машины")

cars_by_brand = Auto.objects.values('brand').annotate(count=Count('id_auto')).order_by('brand')
print("Количество машин каждой марки:")
for car in cars_by_brand:
    print(f"{car['brand']}: {car['count']} машин(ы)")

owners_sorted_by_license_date = AutoOwner.objects.order_by('driverlicense__date_of_issue')
print("Автовладельцы, отсортированные по дате выдачи удостоверения:")
for owner in owners_sorted_by_license_date:
    license_date = DriverLicense.objects.filter(id_owner=owner).values_list('date_of_issue', flat=True).first()
    print(f"{owner.surname} {owner.name}: {license_date}")