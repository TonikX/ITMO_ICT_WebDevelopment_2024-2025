from blog.models import Car, DriverLicence, CarOwner, Ownership, User

def get_cars_by_brand(brand: str):
    return Car.objects.filter(brand=brand)

def get_owners_by_fname(fname: str):
    return CarOwner.objects.filter(first_name=fname)

def get_driver_licence_by_owner(selected_owner: CarOwner):
    return DriverLicence.objects.get(owner_id=selected_owner.id)

def get_owners_by_car_color(color: str):
    return CarOwner.objects.filter(owner_car__car__color=color).distinct()

def get_owners_by_start_year(year: int | str):
    if type(year) == str:
        year = int(year)
    return CarOwner.objects.filter(owner_car__date_of_start__year__gte=year).distinct()
