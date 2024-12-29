from django.shortcuts import render
from django.http import Http404 
from car_owners.models import CarOwner, Car, Ownership, DriverLicense

def owner_detail(request, owner_id):
    owner = CarOwner.objects.get(id=owner_id)  
    return render(request, 'owner.html', {'owner': owner})