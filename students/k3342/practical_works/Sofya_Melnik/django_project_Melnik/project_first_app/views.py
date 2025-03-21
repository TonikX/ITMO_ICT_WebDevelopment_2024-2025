from django.shortcuts import render
from django.http import Http404
from .models import CarOwner


def carowner_detail(request, carowner_id):
    try:
        carowner = CarOwner.objects.get(pk=carowner_id)
    except CarOwner.DoesNotExist:
        raise Http404('CarOwner does not exist')
    return render(request, 'carowner.html', {'carowner': carowner})


