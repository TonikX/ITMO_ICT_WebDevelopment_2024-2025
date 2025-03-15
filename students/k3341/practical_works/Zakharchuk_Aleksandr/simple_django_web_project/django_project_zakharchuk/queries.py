from project_first_app import models

print(models.Car.objects.filter(brand="Toyota"))

print(models.Owner.objects.filter(first_name="John"))

owner = models.Owner.objects.last()
print(models.DriverLicense.objects.get(owner_id=owner))

print(models.Owner.objects.filter(ownership__car_id__color="black"))

print(models.Owner.objects.filter(ownership__start_date__year__gte=2024))
