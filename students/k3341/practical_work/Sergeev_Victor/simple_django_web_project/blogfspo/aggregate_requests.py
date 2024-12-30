from blog.models import Car, DriverLicence, CarOwner, Ownership, User
from django.db.models import Min, Max, Count

def get_oldest_licence():
    return DriverLicence.objects.aggregate(date=Min("date_of_issue"))

def get_nearest_ownership():
    return Ownership.objects.exclude(date_of_finish=None).aggregate(date=Max('date_of_finish'))

def get_car_count_for_owners():
    a = CarOwner.objects.annotate(Count('car'))
    return {f'{o.first_name} {o.last_name}': o.car__count for o in a}

def count_cars_by_brand():
    return Car.objects.values('brand').annotate(Count('id'))

def sort_owners_by_licence_date():
    CarOwner.objects.order_by('owner_licence__date_of_issue')