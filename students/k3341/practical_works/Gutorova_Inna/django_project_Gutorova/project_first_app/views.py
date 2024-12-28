from django.http import Http404
from django.shortcuts import render
from .models import CarOwner  # Import the CarOwner model

def owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)  # Get CarOwner by primary key
    except CarOwner.DoesNotExist:
        raise Http404("Car owner does not exist")
    return render(request, 'owner.html', {'owner': owner})  # Pass the owner object to the template
