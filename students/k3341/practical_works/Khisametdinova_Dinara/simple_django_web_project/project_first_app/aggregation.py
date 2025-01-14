import os
import sys
from django.db.models import Count, Max, Min
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import CarOwner, DriverLicense, Car, CarOwnership

def execute_queries():
    oldest_license = DriverLicense.objects.aggregate(Min('issue_date'))
    print(f"Самая ранняя дата выдачи удостоверения: {oldest_license['issue_date__min']}")

    latest_ownership = CarOwnership.objects.filter(
        car__model__isnull=False
    ).aggregate(Max('end_date'))
    print(f"Самая поздняя дата владения машиной: {latest_ownership['end_date__max']}")

    car_count_per_driver = CarOwner.objects.annotate(car_count=Count('ownerships__car'))
    print("Количество машин у каждого водителя:")
    for owner in car_count_per_driver:
        print(f"Водитель: {owner.username}, Количество машин: {owner.car_count}")

    car_count_per_brand = Car.objects.values('brand').annotate(count=Count('id'))
    print("Количество машин каждой марки:")
    for car in car_count_per_brand:
        print(f"Марка: {car['brand']}, Количество: {car['count']}")

    sorted_owners = DriverLicense.objects.select_related('owner').order_by('issue_date').distinct()
    print("Водители, отсортированные по дате выдачи удостоверения:")
    for license in sorted_owners:
        print(f"Водитель: {license.owner.username}, Дата выдачи: {license.issue_date}")

if __name__ == "__main__":
    execute_queries()
