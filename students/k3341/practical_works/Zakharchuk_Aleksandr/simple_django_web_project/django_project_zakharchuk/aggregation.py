from django.db.models import Count, Max, Min

from project_first_app import models

print(models.DriverLicense.objects.aggregate(oldest_license=Min("issue_date")))

print(models.Ownership.objects.aggregate(latest_license=Max("start_date")))

owners = models.Owner.objects.annotate(car_count=Count("cars"))
for owner in owners:
    print(f"{owner.username}: {owner.car_count}")

print(models.Car.objects.values("brand").annotate(car_count=Count("id")))

print(models.Owner.objects.annotate(first_license=Min("driverlicense__issue_date")).order_by("first_license"))
